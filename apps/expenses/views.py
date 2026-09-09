"""Operating Expense Logging, Approval, and Category Reports Views."""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.expenses.models import Expense, ExpenseCategory
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('expenses')
def expense_list_view(request):
    """Register of branch operating expenses with category filters."""
    branch = request.user.branch
    expenses = Expense.objects.all().select_related('category', 'branch', 'requested_by')
    
    if branch:
        expenses = expenses.filter(branch=branch)
        
    category_id = request.GET.get('category')
    date_filter = request.GET.get('date')
    
    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if date_filter:
        expenses = expenses.filter(expense_date=date_filter)

    categories = ExpenseCategory.objects.all()
    total_amount = sum(e.amount for e in expenses)

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
        'total_amount': total_amount,
        'selected_category': category_id,
        'date_filter': date_filter,
    })

@login_required
@module_permission_required('expenses')
def expense_create_view(request):
    """Log an operational expense voucher."""
    branch = request.user.branch
    categories = ExpenseCategory.objects.all()
    
    if not categories.exists():
        ExpenseCategory.objects.create(name='Kitchen Gas & LPG')
        ExpenseCategory.objects.create(name='Electricity & Water')
        ExpenseCategory.objects.create(name='Packaging & Disposables')
        ExpenseCategory.objects.create(name='Equipment Maintenance')
        ExpenseCategory.objects.create(name='Petty Cash & Housekeeping')
        categories = ExpenseCategory.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        title = request.POST.get('title')
        amount = Decimal(request.POST.get('amount', '0.00'))
        date_str = request.POST.get('expense_date', str(timezone.localdate()))
        payment_mode = request.POST.get('payment_mode', 'CASH')
        notes = request.POST.get('notes', '')

        expense = Expense.objects.create(
            branch=branch or ExpenseCategory.objects.first().expenses.first().branch,
            category_id=category_id,
            title=title,
            amount=amount,
            expense_date=date_str,
            payment_mode=payment_mode,
            requested_by=request.user,
            is_approved=True,  # Direct approval by authorized role
            notes=notes
        )

        messages.success(request, f"Expense '{expense.title}' of ₹{expense.amount} recorded.")
        return redirect('expenses:list')

    return render(request, 'expenses/expense_form.html', {'categories': categories})
