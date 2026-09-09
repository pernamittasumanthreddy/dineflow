"""Supplier Management Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.suppliers.models import Supplier
from apps.suppliers.forms import SupplierForm
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('suppliers')
def supplier_list_view(request):
    """Directory of all contracted raw material vendors."""
    suppliers = Supplier.objects.filter(is_active=True).order_by('company_name')
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})

@login_required
@module_permission_required('suppliers')
def supplier_create_view(request):
    """Add a new vendor with GSTIN and payment terms."""
    form = SupplierForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        supplier = form.save()
        messages.success(request, f"Supplier '{supplier.company_name}' registered.")
        return redirect('suppliers:list')
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'title': 'Add Supplier'})

@login_required
@module_permission_required('suppliers')
def supplier_detail_view(request, supplier_id):
    """View supplier profile, bank details, and purchase history."""
    supplier = get_object_or_404(Supplier, id=supplier_id)
    purchase_orders = supplier.purchase_orders.all()[:10]
    return render(request, 'suppliers/supplier_detail.html', {
        'supplier': supplier,
        'purchase_orders': purchase_orders,
    })
