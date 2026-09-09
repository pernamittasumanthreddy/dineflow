"""Delivery Fleet Logistics, Rider Assignment, and Tracking Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.delivery.models import DeliveryOrder, DeliveryStatus
from apps.accounts.models import User, RoleChoices
from apps.accounts.decorators import module_permission_required

@login_required
def delivery_board_view(request):
    """Delivery dispatch board showing active orders and fleet status."""
    branch = request.user.branch
    deliveries = DeliveryOrder.objects.all().select_related('order', 'assigned_rider')
    
    if branch:
        deliveries = deliveries.filter(order__branch=branch)
        
    status_filter = request.GET.get('status')
    if status_filter:
        deliveries = deliveries.filter(status=status_filter)

    deliveries = deliveries.order_by('-created_at')

    # Available riders
    riders = User.objects.filter(is_active=True).filter(role__in=[RoleChoices.WAITER, RoleChoices.CUSTOMER])

    return render(request, 'delivery/dispatch_board.html', {
        'deliveries': deliveries,
        'riders': riders,
        'statuses': DeliveryStatus.choices,
        'selected_status': status_filter,
    })

@login_required
def delivery_assign_rider_view(request, delivery_id):
    """Assign delivery rider to order."""
    delivery = get_object_or_404(DeliveryOrder, id=delivery_id)
    rider_id = request.POST.get('rider_id')
    
    if rider_id:
        rider = get_object_or_404(User, id=rider_id)
        delivery.assigned_rider = rider
        delivery.status = DeliveryStatus.ASSIGNED
        delivery.save(update_fields=['assigned_rider', 'status'])
        messages.success(request, f"Assigned rider {rider.display_name} to Delivery #{delivery.id}")
    return redirect('delivery:board')

@login_required
def delivery_status_update_view(request, delivery_id):
    """Transition delivery state (OUT_FOR_DELIVERY -> DELIVERED)."""
    delivery = get_object_or_404(DeliveryOrder, id=delivery_id)
    new_status = request.POST.get('status')
    now = timezone.now()

    if new_status in DeliveryStatus.values:
        delivery.status = new_status
        if new_status == DeliveryStatus.OUT_FOR_DELIVERY and not delivery.dispatched_at:
            delivery.dispatched_at = now
        elif new_status == DeliveryStatus.DELIVERED:
            delivery.delivered_at = now
            delivery.order.status = 'COMPLETED'
            delivery.order.save(update_fields=['status'])
        delivery.save()
        messages.success(request, f"Delivery #{delivery.id} status updated to {delivery.get_status_display()}.")

    return redirect('delivery:board')
