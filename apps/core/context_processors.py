"""DineFlow Global Template Context Processors."""
from django.conf import settings

def dineflow_global_context(request):
    """Provides global ERP context variables across all Django templates."""
    context = {
        'APP_NAME': 'DineFlow ERP',
        'APP_VERSION': '2.4.0-Enterprise',
        'CURRENCY_SYMBOL': getattr(settings, 'DEFAULT_CURRENCY_SYMBOL', '₹'),
        'CURRENCY_CODE': getattr(settings, 'DEFAULT_CURRENCY', 'INR'),
        'TIME_ZONE_NAME': getattr(settings, 'TIME_ZONE', 'Asia/Kolkata'),
    }
    
    if request.user.is_authenticated:
        context['current_user'] = request.user
        context['user_role'] = getattr(request.user, 'role', 'GUEST')
        context['user_branch'] = getattr(request.user, 'branch', None)
        try:
            from apps.notifications.models import Notification
            context['unread_notifications_count'] = Notification.objects.filter(
                recipient=request.user, is_read=False
            ).count()
        except Exception:
            context['unread_notifications_count'] = 0
    else:
        context['current_user'] = None
        context['user_role'] = 'ANONYMOUS'
        context['unread_notifications_count'] = 0

    return context
