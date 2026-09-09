"""In-App Notification Center Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.notifications.models import Notification

@login_required
def notification_list_view(request):
    """Notification inbox displaying system alerts, low-stock triggers, and order updates."""
    notifications = Notification.objects.filter(
        models.Q(recipient=request.user) | models.Q(recipient__isnull=True)
    ).order_by('-created_at')[:50]

    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_read_view(request, notification_id):
    """Mark single notification as read and redirect to target URL."""
    notif = get_object_or_404(Notification, id=notification_id)
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    
    if notif.url:
        return redirect(notif.url)
    return redirect('notifications:list')

@login_required
def mark_all_read_view(request):
    """Mark all notifications as read for current user."""
    Notification.objects.filter(
        models.Q(recipient=request.user) | models.Q(recipient__isnull=True),
        is_read=False
    ).update(is_read=True)
    return redirect('notifications:list')
