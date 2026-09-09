"""Sales Registers, Cash Drawer Reconciliation, and End-of-Day Z-Report Views."""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.sales.models import CashRegisterSession, ZReport
from apps.orders.models import Order, OrderStatus
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.expenses.models import Expense
from apps.accounts.decorators import module_permission_required

@login_required
def sales_dashboard_view(request):
    """Real-time sales performance, payment splits, and revenue breakdown."""
    branch = request.user.branch
    today = timezone.localdate()
    
    # Orders today
    orders_qs = Order.objects.filter(created_at__date=today)
    payments_qs = Payment.objects.filter(created_at__date=today, status=PaymentStatus.SUCCESS)
    expenses_qs = Expense.objects.filter(expense_date=today, is_approved=True)

    if branch:
        orders_qs = orders_qs.filter(branch=branch)
        payments_qs = payments_qs.filter(order__branch=branch)
        expenses_qs = expenses_qs.filter(branch=branch)

    total_gross = sum(o.subtotal for o in orders_qs.filter(status=OrderStatus.COMPLETED))
    total_net = sum(o.grand_total for o in orders_qs.filter(status=OrderStatus.COMPLETED))
    total_tax = sum(o.tax_amount for o in orders_qs.filter(status=OrderStatus.COMPLETED))
    total_expenses = sum(e.amount for e in expenses_qs)

    cash_sales = sum(p.amount for p in payments_qs.filter(payment_method=PaymentMethod.CASH))
    upi_sales = sum(p.amount for p in payments_qs.filter(payment_method=PaymentMethod.UPI))
    card_sales = sum(p.amount for p in payments_qs.filter(payment_method=PaymentMethod.CARD))

    return render(request, 'sales/sales_dashboard.html', {
        'total_gross': total_gross,
        'total_net': total_net,
        'total_tax': total_tax,
        'total_expenses': total_expenses,
        'cash_sales': cash_sales,
        'upi_sales': upi_sales,
        'card_sales': card_sales,
        'today': today,
    })

@login_required
@module_permission_required('billing')
def cash_register_view(request):
    """Open or reconcile end-of-shift physical cash drawer."""
    branch = request.user.branch
    active_session = CashRegisterSession.objects.filter(branch=branch, status='OPEN').first() if branch else None

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'OPEN_REGISTER':
            opening_cash = Decimal(request.POST.get('opening_cash', '2000.00'))
            CashRegisterSession.objects.create(
                branch=branch,
                opened_by=request.user,
                opening_cash=opening_cash,
                status='OPEN'
            )
            messages.success(request, f"Cash register opened with float of ₹{opening_cash}.")
            return redirect('sales:register')

        elif action == 'CLOSE_REGISTER' and active_session:
            counted_cash = Decimal(request.POST.get('closing_cash', '0.00'))
            notes = request.POST.get('notes', '')
            
            # Compute expected cash: opening + cash payments today - cash expenses today
            today = timezone.localdate()
            cash_inflows = sum(
                p.amount for p in Payment.objects.filter(
                    order__branch=branch,
                    created_at__gte=active_session.opened_at,
                    payment_method=PaymentMethod.CASH,
                    status=PaymentStatus.SUCCESS
                )
            )
            cash_outflows = sum(
                e.amount for e in Expense.objects.filter(
                    branch=branch,
                    created_at__gte=active_session.opened_at,
                    payment_mode='CASH',
                    is_approved=True
                )
            )
            expected = active_session.opening_cash + cash_inflows - cash_outflows
            discrepancy = counted_cash - expected

            active_session.closed_by = request.user
            active_session.closing_cash = counted_cash
            active_session.expected_cash = expected
            active_session.cash_discrepancy = discrepancy
            active_session.status = 'CLOSED'
            active_session.closed_at = timezone.now()
            active_session.notes = notes
            active_session.save()

            messages.success(request, f"Register closed. Counted: ₹{counted_cash}, Expected: ₹{expected}, Difference: ₹{discrepancy}")
            return redirect('sales:register')

    return render(request, 'sales/cash_register.html', {'active_session': active_session})

@login_required
@module_permission_required('billing')
def daily_z_report_view(request):
    """End-of-day statutory Z-Report generator and printer view."""
    branch = request.user.branch
    today = timezone.localdate()

    if not branch:
        messages.error(request, "Please switch to an active branch context to run Z-Report.")
        return redirect('core:dashboard')

    z_report, created = ZReport.objects.get_or_create(
        branch=branch,
        report_date=today,
        defaults={
            'gross_sales': Decimal('0.00'),
            'net_sales': Decimal('0.00'),
            'net_drawer_balance': Decimal('0.00'),
            'generated_by': request.user
        }
    )

    # Calculate real-time day numbers
    orders_qs = Order.objects.filter(branch=branch, created_at__date=today, status=OrderStatus.COMPLETED)
    payments_qs = Payment.objects.filter(order__branch=branch, created_at__date=today, status=PaymentStatus.SUCCESS)
    expenses_qs = Expense.objects.filter(branch=branch, expense_date=today, is_approved=True)

    z_report.total_orders = orders_qs.count()
    z_report.gross_sales = sum(o.subtotal for o in orders_qs)
    z_report.discount_total = sum(o.discount_amount for o in orders_qs)
    z_report.tax_total = sum(o.tax_amount for o in orders_qs)
    z_report.net_sales = sum(o.grand_total for o in orders_qs)

    z_report.cash_sales = sum(p.amount for p in payments_qs.filter(payment_method=PaymentMethod.CASH))
    z_report.card_sales = sum(p.amount for p in payments_qs.filter(payment_method=PaymentMethod.CARD))
    z_report.upi_sales = sum(p.amount for p in payments_qs.filter(payment_method=PaymentMethod.UPI))

    z_report.total_expenses = sum(e.amount for e in expenses_qs)
    z_report.net_drawer_balance = z_report.cash_sales - z_report.total_expenses
    z_report.save()

    return render(request, 'sales/z_report.html', {'z_report': z_report})
