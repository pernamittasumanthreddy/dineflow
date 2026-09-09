"""Global Enterprise Context Processor for DineFlow Templates."""
from django.utils import timezone
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.orders.models import Order, OrderStatus
from apps.inventory.models import Ingredient
from apps.notifications.models import Notification

def dineflow_global_context(request):
    """
    Supplies global ERP state to all templates:
    - Active restaurant and branch details
    - Live pending kitchen order count
    - Current low-stock warning count
    - Unread notification count
    - Server current time in Asia/Kolkata
    """
    context = {
        'current_server_time': timezone.localtime(),
        'app_name': 'DineFlow Enterprise ERP',
        'active_branch': None,
        'pending_kds_count': 0,
        'low_stock_count': 0,
        'unread_notif_count': 0,
    }

    if request.user.is_authenticated:
        branch = getattr(request.user, 'branch', None)
        if not branch:
            branch = Branch.objects.first()
        context['active_branch'] = branch

        # Live operational counters
        if branch:
            context['pending_kds_count'] = Order.objects.filter(
                branch=branch,
                status__in=[OrderStatus.NEW, OrderStatus.CONFIRMED, OrderStatus.PREPARING]
            ).count()
            context['low_stock_count'] = Ingredient.objects.filter(
                branch=branch,
                current_stock__lte=models_F('minimum_stock_level')
            ).count()

        context['unread_notif_count'] = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

    return context

def models_F(field_name):
    """Helper to avoid top-level import cycles if needed."""
    from django.db.models import F
    return F(field_name)
