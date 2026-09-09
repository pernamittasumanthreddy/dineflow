"""Kitchen Display System (KDS) and Expeditor Bump Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.kitchen.models import KitchenTicket, TicketStatus, KitchenStation
from apps.orders.models import Order, OrderStatus
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('kitchen')
def kds_board_view(request):
    """
    Live Kitchen Display System (KDS) board.
    Displays color-coded active tickets, dish modifications, and time elapsed.
    """
    branch = request.user.branch
    station_filter = request.GET.get('station', KitchenStation.ALL)
    
    # Sync: automatically create tickets for confirmed orders that don't have one yet
    unattached_orders = Order.objects.filter(
        status__in=[OrderStatus.CONFIRMED, OrderStatus.PREPARING],
        kitchen_tickets__isnull=True
    )
    if branch:
        unattached_orders = unattached_orders.filter(branch=branch)
        
    for ord_obj in unattached_orders:
        max_prep = max([it.menu_item.preparation_time_minutes for it in ord_obj.items.all()] or [15])
        KitchenTicket.objects.create(
            order=ord_obj,
            ticket_number=f"KOT-{ord_obj.order_number[-6:]}",
            station=KitchenStation.ALL,
            expected_prep_minutes=max_prep,
            status=TicketStatus.PENDING
        )

    tickets_qs = KitchenTicket.objects.filter(
        status__in=[TicketStatus.PENDING, TicketStatus.PREPARING, TicketStatus.READY]
    ).select_related('order__table', 'order__branch').prefetch_related('order__items__menu_item')

    if branch:
        tickets_qs = tickets_qs.filter(order__branch=branch)
    if station_filter and station_filter != KitchenStation.ALL:
        tickets_qs = tickets_qs.filter(station=station_filter)

    tickets_qs = tickets_qs.order_by('created_at')

    # Metrics
    total_active = tickets_qs.count()
    delayed_count = sum(1 for t in tickets_qs if t.is_delayed)
    avg_prep = 0
    completed_today = KitchenTicket.objects.filter(
        created_at__date=timezone.localdate(),
        completed_cooking_at__isnull=False
    )
    if completed_today.exists():
        total_time = sum(t.elapsed_minutes for t in completed_today)
        avg_prep = int(total_time / completed_today.count())

    return render(request, 'kitchen/kds.html', {
        'tickets': tickets_qs,
        'station_filter': station_filter,
        'stations': KitchenStation.choices,
        'total_active': total_active,
        'delayed_count': delayed_count,
        'avg_prep': avg_prep,
    })

@login_required
@module_permission_required('kitchen')
def ticket_bump_view(request, ticket_id):
    """Bumps ticket to next station state: PENDING -> PREPARING -> READY -> BUMPED."""
    ticket = get_object_or_404(KitchenTicket, id=ticket_id)
    now = timezone.now()

    if ticket.status == TicketStatus.PENDING:
        ticket.status = TicketStatus.PREPARING
        ticket.started_cooking_at = now
        ticket.order.status = OrderStatus.PREPARING
        ticket.order.prep_started_at = now
        ticket.order.save(update_fields=['status', 'prep_started_at'])
        messages.info(request, f"Ticket #{ticket.ticket_number} marked Cooking.")
    elif ticket.status == TicketStatus.PREPARING:
        ticket.status = TicketStatus.READY
        ticket.completed_cooking_at = now
        ticket.order.status = OrderStatus.READY
        ticket.order.ready_at = now
        ticket.order.save(update_fields=['status', 'ready_at'])
        messages.success(request, f"Ticket #{ticket.ticket_number} is READY for serving!")
    elif ticket.status == TicketStatus.READY:
        ticket.status = TicketStatus.BUMPED
        ticket.bumped_at = now
        ticket.bumped_by = request.user
        messages.success(request, f"Ticket #{ticket.ticket_number} bumped/cleared.")

    ticket.save()
    return redirect(request.META.get('HTTP_REFERER') or 'kitchen:kds')

@login_required
@module_permission_required('kitchen')
def kitchen_performance_view(request):
    """Analytics on kitchen SLAs, station preparation times, and delays."""
    today = timezone.localdate()
    today_tickets = KitchenTicket.objects.filter(created_at__date=today)
    
    total_tickets = today_tickets.count()
    completed_tickets = today_tickets.filter(status__in=[TicketStatus.READY, TicketStatus.BUMPED])
    delayed_tickets = [t for t in today_tickets if t.is_delayed]
    
    avg_duration = 0
    if completed_tickets.exists():
        avg_duration = sum(t.elapsed_minutes for t in completed_tickets) / completed_tickets.count()

    return render(request, 'kitchen/performance.html', {
        'total_tickets': total_tickets,
        'completed_count': completed_tickets.count(),
        'delayed_count': len(delayed_tickets),
        'avg_duration': round(avg_duration, 1),
        'today_tickets': today_tickets.order_by('-created_at')[:25],
    })
