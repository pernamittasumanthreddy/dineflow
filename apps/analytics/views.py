"""Executive Business Intelligence, RevPASH, and Profitability Analytics Views."""
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.expenses.models import Expense
from apps.tables.models import RestaurantTable
from apps.menu.models import MenuItem, Category
from apps.branches.models import Branch
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('analytics')
def analytics_dashboard_view(request):
    """
    Comprehensive Restaurant Executive Dashboard.
    Calculates RevPASH, COGS, Table Turnover, Best Sellers, and Hourly Trends.
    """
    branch = request.user.branch
    today = timezone.localdate()
    
    # 30-Day Window Analysis
    start_date = today - timezone.timedelta(days=30)
    
    completed_orders = Order.objects.filter(
        created_at__date__gte=start_date,
        status=OrderStatus.COMPLETED
    )
    all_expenses = Expense.objects.filter(
        expense_date__gte=start_date,
        is_approved=True
    )

    if branch:
        completed_orders = completed_orders.filter(branch=branch)
        all_expenses = all_expenses.filter(branch=branch)

    # Core Financials
    total_revenue = sum(o.grand_total for o in completed_orders) or Decimal('0.00')
    total_expenses = sum(e.amount for e in all_expenses) or Decimal('0.00')
    net_profit = total_revenue - total_expenses
    order_count = completed_orders.count()
    aov = (total_revenue / order_count).quantize(Decimal('0.01')) if order_count > 0 else Decimal('0.00')

    # RevPASH Calculation (Revenue Per Available Seat Hour)
    # RevPASH = Total Revenue / (Total Seating Capacity * Operating Hours per day * Days in period)
    tables = RestaurantTable.objects.all()
    if branch:
        tables = tables.filter(branch=branch)
    total_seats = sum(t.seating_capacity for t in tables) or 50
    operating_hours = 12.0  # 11:00 AM to 11:00 PM
    total_available_seat_hours = total_seats * operating_hours * 30
    revpash = (float(total_revenue) / total_available_seat_hours) if total_available_seat_hours > 0 else 0.0

    # Table Turnover Rate = Total Orders / (Total Tables * Days)
    total_tables_count = tables.count() or 1
    table_turnover = round(order_count / (total_tables_count * 30), 2)

    # Best-Selling Dishes
    best_sellers = (
        OrderItem.objects.filter(order__in=completed_orders)
        .values('menu_item__name', 'menu_item__food_type')
        .annotate(total_sold=Sum('quantity'), revenue=Sum('item_total'))
        .order_by('-total_sold')[:8]
    )

    # Category Revenue Distribution
    category_sales = (
        OrderItem.objects.filter(order__in=completed_orders)
        .values('menu_item__category__name')
        .annotate(cat_revenue=Sum('item_total'))
        .order_by('-cat_revenue')[:6]
    )

    return render(request, 'analytics/dashboard.html', {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'order_count': order_count,
        'aov': aov,
        'revpash': round(revpash, 2),
        'table_turnover': table_turnover,
        'best_sellers': best_sellers,
        'category_sales': category_sales,
        'total_seats': total_seats,
    })
