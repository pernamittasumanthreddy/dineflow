"""Analytics & Business Intelligence Aggregation Services."""
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.expenses.models import Expense
from apps.payments.models import Payment, PaymentStatus
from apps.analytics.models import DailyAnalyticsSnapshot

def compute_daily_snapshot(branch, target_date=None):
    """
    Aggregates orders and expenses for a single calendar day into DailyAnalyticsSnapshot.
    Computes Gross Revenue, Expenses, Net Profit, Order Count, Covers, and AOV.
    """
    if target_date is None:
        target_date = timezone.localdate()

    orders = Order.objects.filter(
        branch=branch,
        created_at__date=target_date,
        status=OrderStatus.COMPLETED
    )
    order_count = orders.count()
    revenue_data = orders.aggregate(
        total_rev=Sum('grand_total'),
        total_covers=Sum('guest_count')
    )
    gross_revenue = revenue_data['total_rev'] or Decimal('0.00')
    guest_covers = revenue_data['total_covers'] or 0

    expenses = Expense.objects.filter(
        branch=branch,
        expense_date=target_date,
        is_approved=True
    )
    total_expenses = expenses.aggregate(tot=Sum('amount'))['tot'] or Decimal('0.00')

    net_profit = gross_revenue - total_expenses
    aov = (gross_revenue / Decimal(str(order_count))) if order_count > 0 else Decimal('0.00')

    snapshot, _ = DailyAnalyticsSnapshot.objects.update_or_create(
        branch=branch,
        date=target_date,
        defaults={
            'total_revenue': gross_revenue,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'order_count': order_count,
            'guest_covers': guest_covers,
            'average_order_value': aov.quantize(Decimal('0.01')),
        }
    )
    return snapshot

def get_top_selling_dishes(branch=None, limit=5, days=30):
    """
    Ranks menu items by quantity sold and total revenue generated over the last N days.
    """
    cutoff = timezone.now() - timedelta(days=days)
    qs = OrderItem.objects.filter(
        order__created_at__gte=cutoff,
        order__status=OrderStatus.COMPLETED
    )
    if branch:
        qs = qs.filter(order__branch=branch)

    top_items = qs.values(
        'menu_item__name',
        'menu_item__code'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('item_total')
    ).order_by('-total_revenue')[:limit]

    return list(top_items)

def get_sales_summary(branch=None, days=30):
    """
    Returns aggregated KPIs for the past N days.
    """
    cutoff = timezone.now() - timedelta(days=days)
    qs = Order.objects.filter(
        created_at__gte=cutoff,
        status=OrderStatus.COMPLETED
    )
    if branch:
        qs = qs.filter(branch=branch)

    agg = qs.aggregate(
        total_revenue=Sum('grand_total'),
        total_subtotal=Sum('subtotal'),
        total_tax=Sum('tax_amount'),
        total_discounts=Sum('discount_amount'),
        total_orders=Count('id')
    )
    total_orders = agg['total_orders'] or 0
    total_rev = agg['total_revenue'] or Decimal('0.00')
    aov = (total_rev / Decimal(str(total_orders))) if total_orders > 0 else Decimal('0.00')

    return {
        'total_revenue': total_rev,
        'total_subtotal': agg['total_subtotal'] or Decimal('0.00'),
        'total_tax': agg['total_tax'] or Decimal('0.00'),
        'total_discounts': agg['total_discounts'] or Decimal('0.00'),
        'total_orders': total_orders,
        'aov': aov.quantize(Decimal('0.01')),
    }

def get_payment_method_breakdown(branch=None, days=30):
    """
    Calculates percentage split across UPI, Cash, and Card payments.
    """
    cutoff = timezone.now() - timedelta(days=days)
    qs = Payment.objects.filter(
        created_at__gte=cutoff,
        status=PaymentStatus.SUCCESS
    )
    if branch:
        qs = qs.filter(order__branch=branch)

    breakdown = qs.values('payment_method').annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    ).order_by('-total_amount')

    return list(breakdown)
