"""Core Navigation, Error Handlers, and Global Dashboard Controller."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models

def home_redirect_view(request):
    """Redirect to dashboard if logged in, otherwise to login."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    """
    Central Executive & Operational ERP Dashboard.
    Adapts metrics and quick actions dynamically according to the user's role.
    """
    user = request.user
    role = user.role
    
    # Safe metric imports with defaults
    total_orders_today = 0
    total_sales_today = 0.0
    active_tables_count = 0
    pending_kds_count = 0
    low_stock_count = 0
    recent_orders = []
    
    try:
        from apps.orders.models import Order, OrderStatus
        from apps.tables.models import RestaurantTable, TableStatus
        from apps.inventory.models import Ingredient
        from django.utils import timezone
        
        today = timezone.localdate()
        today_orders = Order.objects.filter(created_at__date=today)
        if user.branch:
            today_orders = today_orders.filter(branch=user.branch)
            
        total_orders_today = today_orders.count()
        total_sales_today = sum(o.grand_total for o in today_orders.filter(status=OrderStatus.COMPLETED))
        
        tables_qs = RestaurantTable.objects.all()
        if user.branch:
            tables_qs = tables_qs.filter(branch=user.branch)
        active_tables_count = tables_qs.filter(status=TableStatus.OCCUPIED).count()
        
        pending_kds_count = today_orders.filter(status__in=[OrderStatus.CONFIRMED, OrderStatus.PREPARING]).count()
        
        low_stock_count = Ingredient.objects.filter(current_stock__lte=models.F('reorder_level')).count() if hasattr(Ingredient, 'reorder_level') else 0
        recent_orders = today_orders.order_by('-created_at')[:8]
    except Exception:
        pass

    context = {
        'page_title': 'Enterprise Operations Dashboard',
        'role': role,
        'total_orders_today': total_orders_today,
        'total_sales_today': total_sales_today,
        'active_tables_count': active_tables_count,
        'pending_kds_count': pending_kds_count,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
    }
    return render(request, 'core/dashboard.html', context)

def bad_request_view(request, exception=None):
    """Custom 400 Bad Request error page."""
    return render(request, 'errors/400.html', {'error_message': str(exception) if exception else 'Bad Request'}, status=400)

def permission_denied_view(request, exception=None):
    """Custom 403 Forbidden error page."""
    return render(request, 'errors/403.html', {'error_message': str(exception) if exception else 'Access Denied'}, status=403)

def page_not_found_view(request, exception=None):
    """Custom 404 Not Found error page."""
    return render(request, 'errors/404.html', {'path': request.path}, status=404)

def server_error_view(request):
    """Custom 500 Internal Server Error page."""
    return render(request, 'errors/500.html', status=500)
