"""POS Terminal, Cart Engine, and Order Lifecycle Management Views."""
import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from apps.orders.models import Order, OrderItem, OrderType, OrderStatus
from apps.orders.forms import OrderCreateForm, OrderCancelForm
from apps.tables.models import RestaurantTable, TableStatus
from apps.menu.models import Category, MenuItem, MenuItemVariant
from apps.customers.models import Customer
from apps.accounts.decorators import module_permission_required

@login_required
def pos_terminal_view(request):
    """
    High-speed touchscreen POS order-taking terminal.
    Allows waiters/cashiers to pick tables, customize dishes, and fire orders to KDS.
    """
    branch = request.user.branch
    categories = Category.objects.filter(is_active=True).prefetch_related('items__variants')
    tables = RestaurantTable.objects.filter(is_active=True)
    customers = Customer.objects.all().order_by('-created_at')[:20]
    
    if branch:
        tables = tables.filter(branch=branch)

    if request.method == 'POST':
        # Process order creation from POS payload
        try:
            order_type = request.POST.get('order_type', OrderType.DINE_IN)
            table_id = request.POST.get('table_id')
            customer_phone = request.POST.get('customer_phone')
            customer_name = request.POST.get('customer_name')
            cart_data = json.loads(request.POST.get('cart_json', '[]'))
            special_instructions = request.POST.get('special_instructions', '')
            
            if not cart_data:
                messages.error(request, "Cannot place an empty order.")
                return redirect('orders:pos')
                
            # Customer resolution
            customer = None
            if customer_phone:
                customer, _ = Customer.objects.get_or_create(
                    phone=customer_phone,
                    defaults={'name': customer_name or 'Walk-in Guest'}
                )

            # Table resolution
            table = None
            if order_type == OrderType.DINE_IN and table_id:
                table = RestaurantTable.objects.filter(id=table_id).first()

            # Sequence number generation
            today_str = timezone.localdate().strftime('%Y%m%d')
            order_count = Order.objects.filter(created_at__date=timezone.localdate()).count() + 1
            order_num = f"ORD-{today_str}-{order_count:04d}"

            # Create Order
            order = Order.objects.create(
                order_number=order_num,
                order_type=order_type,
                status=OrderStatus.CONFIRMED,
                branch=branch or (table.branch if table else None),
                table=table,
                customer=customer,
                server=request.user,
                special_instructions=special_instructions,
                confirmed_at=timezone.now()
            )

            # Add Line Items
            for item in cart_data:
                menu_item = MenuItem.objects.get(id=item['item_id'])
                variant = MenuItemVariant.objects.filter(id=item.get('variant_id')).first() if item.get('variant_id') else None
                qty = int(item.get('qty', 1))
                unit_price = variant.price if variant else menu_item.base_price
                
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    variant=variant,
                    quantity=qty,
                    unit_price=unit_price,
                    kitchen_notes=item.get('notes', '')
                )

            # Recalculate financial totals
            order.recalculate_totals()

            # Mark table as occupied
            if table:
                table.status = TableStatus.OCCUPIED
                table.current_order = order
                table.save(update_fields=['status', 'current_order'])

            # Trigger in-app notification
            try:
                from apps.notifications.models import Notification
                Notification.objects.create(
                    title=f"New Order #{order.order_number}",
                    message=f"Order placed for {order.get_order_type_display()} - ₹{order.grand_total}",
                    notification_type='NEW_ORDER',
                    url=f"/orders/{order.id}/"
                )
            except Exception:
                pass

            messages.success(request, f"Order #{order.order_number} sent to Kitchen successfully!")
            return redirect('orders:detail', order_id=order.id)
        except Exception as e:
            messages.error(request, f"Failed to place order: {str(e)}")
            return redirect('orders:pos')

    return render(request, 'orders/pos.html', {
        'categories': categories,
        'tables': tables,
        'customers': customers,
        'order_types': OrderType.choices,
    })

@login_required
def order_list_view(request):
    """View active and historical orders with comprehensive filters."""
    branch = request.user.branch
    orders = Order.objects.all().select_related('table', 'customer', 'server', 'branch')
    
    if branch:
        orders = orders.filter(branch=branch)
        
    status_filter = request.GET.get('status')
    order_type_filter = request.GET.get('type')
    date_filter = request.GET.get('date')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    if order_type_filter:
        orders = orders.filter(order_type=order_type_filter)
    if date_filter:
        orders = orders.filter(created_at__date=date_filter)

    orders = orders.order_by('-created_at')

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'status_filter': status_filter,
        'type_filter': order_type_filter,
        'statuses': OrderStatus.choices,
        'order_types': OrderType.choices,
    })

@login_required
def order_detail_view(request, order_id):
    """Detailed view of an order with line items, tax, and actions."""
    order = get_object_or_404(Order.objects.select_related('table', 'customer', 'server', 'branch'), id=order_id)
    items = order.items.all().select_related('menu_item', 'variant')
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'statuses': OrderStatus.choices,
    })

@login_required
def order_update_status_view(request, order_id):
    """Move order across lifecycle states (e.g. PREPARING -> READY -> COMPLETED)."""
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in OrderStatus.values:
        order.status = new_status
        now = timezone.now()
        
        if new_status == OrderStatus.PREPARING and not order.prep_started_at:
            order.prep_started_at = now
        elif new_status == OrderStatus.READY and not order.ready_at:
            order.ready_at = now
        elif new_status == OrderStatus.COMPLETED:
            order.completed_at = now
            # Release table
            if order.table:
                order.table.status = TableStatus.CLEANING
                order.table.current_order = None
                order.table.save(update_fields=['status', 'current_order'])
                
            # Deduct inventory for recipes consumed
            try:
                from apps.inventory.models import StockMovement, MovementType
                for line_item in order.items.all():
                    for recipe in line_item.menu_item.recipe_ingredients.all():
                        if recipe.ingredient:
                            ing = recipe.ingredient
                            qty_consumed = Decimal(str(recipe.quantity_required)) * Decimal(str(line_item.quantity))
                            old_stock = ing.current_stock
                            ing.current_stock = max(Decimal('0.000'), ing.current_stock - qty_consumed)
                            ing.save(update_fields=['current_stock'])
                            
                            StockMovement.objects.create(
                                ingredient=ing,
                                movement_type=MovementType.ORDER_CONSUMPTION,
                                quantity=-qty_consumed,
                                stock_before=old_stock,
                                stock_after=ing.current_stock,
                                reference_id=f"ORD-{order.order_number}",
                                recorded_by=request.user,
                                notes=f"Auto recipe deduction for {line_item.quantity}x {line_item.menu_item.name}"
                            )
            except Exception:
                pass

        order.save()
        messages.success(request, f"Order #{order.order_number} is now {order.get_status_display()}.")
    return redirect(request.META.get('HTTP_REFERER') or 'orders:detail', order_id=order.id)

@login_required
def order_cancel_view(request, order_id):
    """Cancel order with mandatory explanation and release table."""
    order = get_object_or_404(Order, id=order_id)
    form = OrderCancelForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        order.status = OrderStatus.CANCELLED
        order.cancellation_reason = form.cleaned_data['reason']
        order.save(update_fields=['status', 'cancellation_reason'])
        
        if order.table:
            order.table.status = TableStatus.AVAILABLE
            order.table.current_order = None
            order.table.save(update_fields=['status', 'current_order'])
            
        messages.warning(request, f"Order #{order.order_number} has been cancelled.")
        return redirect('orders:detail', order_id=order.id)

    return render(request, 'orders/order_cancel.html', {'order': order, 'form': form})
