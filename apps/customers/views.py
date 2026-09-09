"""Customer CRM, Dining Profile, and Lifetime Spend Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.db.models import Q
from apps.customers.models import Customer
from apps.accounts.decorators import module_permission_required

@login_required
def customer_list_view(request):
    """Guest directory with total visits and lifetime value."""
    search_q = request.GET.get('q')
    customers = Customer.objects.all()
    if search_q:
        customers = customers.filter(
            models.Q(name__icontains=search_q) |
            models.Q(phone__icontains=search_q) |
            models.Q(email__icontains=search_q)
        )
    customers = customers.order_by('-total_spent')[:50]
    return render(request, 'customers/customer_list.html', {'customers': customers, 'search_q': search_q})

@login_required
def customer_detail_view(request, customer_id):
    """Customer profile showing order history, dietary preferences, and loyalty balance."""
    customer = get_object_or_404(Customer, id=customer_id)
    orders = customer.orders.all().order_by('-created_at')[:15]
    reservations = customer.reservations.all().order_by('-created_at')[:10]
    loyalty = getattr(customer, 'loyalty_account', None)
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'reservations': reservations,
        'loyalty': loyalty,
    })
