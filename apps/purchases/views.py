"""Purchase Order Execution, Goods Receiving, and Auto-Stock Intake Views."""
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.purchases.models import PurchaseOrder, PurchaseOrderItem, POStatus
from apps.suppliers.models import Supplier
from apps.inventory.models import Ingredient, StockMovement, MovementType
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('purchases')
def po_list_view(request):
    """Register of all procurement orders and delivery fulfillment states."""
    branch = request.user.branch
    pos = PurchaseOrder.objects.all().select_related('supplier', 'branch', 'created_by')
    
    if branch:
        pos = pos.filter(branch=branch)
        
    status_filter = request.GET.get('status')
    if status_filter:
        pos = pos.filter(status=status_filter)
        
    pos = pos.order_by('-created_at')

    return render(request, 'purchases/po_list.html', {
        'pos': pos,
        'status_filter': status_filter,
        'statuses': POStatus.choices,
    })

@login_required
@module_permission_required('purchases')
def po_create_view(request):
    """Raise a new purchase order for kitchen provisions."""
    branch = request.user.branch
    suppliers = Supplier.objects.filter(is_active=True)
    ingredients = Ingredient.objects.filter(is_active=True)
    if branch:
        ingredients = ingredients.filter(branch=branch)

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        expected_date = request.POST.get('expected_delivery_date') or None
        notes = request.POST.get('notes', '')
        
        now = timezone.now()
        po_count = PurchaseOrder.objects.count() + 1
        po_num = f"PO-{now.strftime('%Y%m')}-{po_count:04d}"

        po = PurchaseOrder.objects.create(
            po_number=po_num,
            supplier_id=supplier_id,
            branch=branch or ingredients.first().branch,
            order_date=now.date(),
            expected_delivery_date=expected_date,
            status=POStatus.APPROVED,  # Approved for fulfillment
            created_by=request.user,
            notes=notes
        )

        # Parse submitted ingredients
        ingredient_ids = request.POST.getlist('ingredient_id[]')
        quantities = request.POST.getlist('quantity[]')
        rates = request.POST.getlist('rate[]')

        for i in range(len(ingredient_ids)):
            if ingredient_ids[i] and quantities[i]:
                ing = Ingredient.objects.get(id=ingredient_ids[i])
                qty = Decimal(quantities[i])
                rate = Decimal(rates[i]) if (i < len(rates) and rates[i]) else ing.unit_cost
                
                PurchaseOrderItem.objects.create(
                    purchase_order=po,
                    ingredient=ing,
                    ordered_quantity=qty,
                    unit_cost=rate,
                    gst_rate_percent=Decimal('5.00')
                )

        po.recalculate_totals()
        messages.success(request, f"Purchase Order #{po.po_number} raised successfully for ₹{po.total_amount}.")
        return redirect('purchases:detail', po_id=po.id)

    return render(request, 'purchases/po_form.html', {
        'suppliers': suppliers,
        'ingredients': ingredients,
    })

@login_required
@module_permission_required('purchases')
def po_detail_view(request, po_id):
    """View purchase order invoice and line item delivery status."""
    po = get_object_or_404(PurchaseOrder.objects.select_related('supplier', 'branch', 'created_by', 'approved_by', 'received_by'), id=po_id)
    items = po.items.all().select_related('ingredient')
    return render(request, 'purchases/po_detail.html', {
        'po': po,
        'items': items,
        'statuses': POStatus.choices,
    })

@login_required
@module_permission_required('purchases')
def po_receive_goods_view(request, po_id):
    """
    Inward verification: marks PO as RECEIVED, updates physical stock, and writes to audit ledger.
    """
    po = get_object_or_404(PurchaseOrder, id=po_id)
    
    if po.status == POStatus.RECEIVED:
        messages.warning(request, "This purchase order has already been received.")
        return redirect('purchases:detail', po_id=po.id)

    now = timezone.now()
    po.status = POStatus.RECEIVED
    po.received_by = request.user
    po.received_at = now
    po.save(update_fields=['status', 'received_by', 'received_at'])

    # Increment stock for each item
    for item in po.items.all():
        ing = item.ingredient
        received_qty = item.ordered_quantity  # Full delivery assumption unless split
        item.received_quantity = received_qty
        item.save(update_fields=['received_quantity'])

        old_stock = ing.current_stock
        ing.current_stock += received_qty
        ing.save(update_fields=['current_stock'])

        StockMovement.objects.create(
            ingredient=ing,
            movement_type=MovementType.PURCHASE_RECEIPT,
            quantity=received_qty,
            stock_before=old_stock,
            stock_after=ing.current_stock,
            reference_id=f"PO-{po.po_number}",
            recorded_by=request.user,
            notes=f"Inward intake from {po.supplier.company_name}"
        )

    messages.success(request, f"PO #{po.po_number} received. Stock levels have been automatically updated.")
    return redirect('purchases:detail', po_id=po.id)
