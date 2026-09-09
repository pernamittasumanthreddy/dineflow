from django.shortcuts import render

def ledger(request):
    """
    Daily Petty Cash & Expense Ledger.
    """
    expenses = [
        {'id': 'EXP-1041', 'date': '09/09/2026, 08:30 AM', 'category': 'Vegetable Mandi Market', 'title': 'Fresh Mint, Coriander, Ginger & Garlic', 'amount': 850.00, 'paid_by': 'Petty Cash', 'approved_by': 'Chef Sanjeev', 'status': 'paid'},
        {'id': 'EXP-1042', 'date': '08/09/2026', 'category': 'Kitchen Equipment AMC', 'title': 'Tandoor Blower Motor Maintenance', 'amount': 1400.00, 'paid_by': 'UPI / Netbanking', 'approved_by': 'Pavan Varma', 'status': 'paid'},
        {'id': 'EXP-1043', 'date': '07/09/2026', 'category': 'Cleaning & Sanitation', 'title': 'Food-Grade Sanitizers & Dishwashing Liquids', 'amount': 2100.00, 'paid_by': 'UPI / Netbanking', 'approved_by': 'Sneha Reddy', 'status': 'paid'},
        {'id': 'EXP-1044', 'date': '05/09/2026', 'category': 'Utilities & Fuel', 'title': 'Commercial LPG Gas Cylinders (4 x 19kg)', 'amount': 7200.00, 'paid_by': 'Bank Transfer', 'approved_by': 'Pavan Varma', 'status': 'paid'},
    ]
    context = {
        'page_title': 'Expense & Petty Cash Ledger',
        'expenses': expenses
    }
    return render(request, 'expenses/ledger.html', context)
