"""Table Reservations and Guest Booking Controller."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.reservations.models import Reservation, ReservationStatus
from apps.reservations.forms import ReservationForm
from apps.tables.models import RestaurantTable, TableStatus
from apps.branches.models import Branch

@login_required
def reservation_list_view(request):
    """List of reservations with date filters and status updates."""
    branch = request.user.branch
    today = timezone.localdate()
    
    selected_date = request.GET.get('date', str(today))
    status_filter = request.GET.get('status')
    
    reservations = Reservation.objects.all().select_related('assigned_table', 'branch')
    if branch:
        reservations = reservations.filter(branch=branch)
        
    if selected_date:
        reservations = reservations.filter(reservation_date=selected_date)
    if status_filter:
        reservations = reservations.filter(status=status_filter)
        
    reservations = reservations.order_by('reservation_time')
    
    return render(request, 'reservations/reservation_list.html', {
        'reservations': reservations,
        'selected_date': selected_date,
        'status_filter': status_filter,
        'statuses': ReservationStatus.choices,
    })

@login_required
def reservation_create_view(request):
    """Create a new reservation for a guest."""
    form = ReservationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        res = form.save(commit=False)
        res.branch = request.user.branch or Branch.objects.first()
        res.booked_by_staff = request.user
        res.save()
        
        # Optionally reserve the assigned table
        if res.assigned_table and res.status in [ReservationStatus.CONFIRMED, ReservationStatus.PENDING]:
            res.assigned_table.status = TableStatus.RESERVED
            res.assigned_table.save(update_fields=['status'])
            
        messages.success(request, f"Reservation for {res.guest_name} booked for {res.reservation_date} at {res.reservation_time}.")
        return redirect('reservations:list')
    return render(request, 'reservations/reservation_form.html', {'form': form, 'title': 'New Reservation'})

@login_required
def reservation_status_update_view(request, reservation_id):
    """Transition reservation state (Confirm, Seat, Cancel, No-Show)."""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    new_status = request.POST.get('status')
    
    if new_status in ReservationStatus.values:
        reservation.status = new_status
        reservation.save(update_fields=['status'])
        
        # Update associated table if guest is seated or cancelled
        if reservation.assigned_table:
            if new_status == ReservationStatus.SEATED:
                reservation.assigned_table.status = TableStatus.OCCUPIED
                reservation.assigned_table.save(update_fields=['status'])
            elif new_status in [ReservationStatus.CANCELLED, ReservationStatus.NO_SHOW, ReservationStatus.COMPLETED]:
                reservation.assigned_table.status = TableStatus.AVAILABLE
                reservation.assigned_table.save(update_fields=['status'])
                
        messages.success(request, f"Reservation #{reservation.id} status updated to {reservation.get_status_display()}.")
    return redirect(request.META.get('HTTP_REFERER') or 'reservations:list')
