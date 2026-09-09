from django.shortcuts import render

def invoices(request):
    """
    Indian GST Tax Invoices Master Ledger.
    """
    invoices_list = [
        {'inv_num': 'INV-892401', 'date': '09/09/2026, 14:32', 'table': 'T-04 (AC Hall)', 'customer': 'Dr. Anjali Sharma', 'subtotal': 1200.00, 'cgst': 30.00, 'sgst': 30.00, 'grand_total': 1260.00, 'payment_mode': 'UPI', 'status': 'paid'},
        {'inv_num': 'INV-892400', 'date': '09/09/2026, 14:18', 'table': 'T-08 (Terrace)', 'customer': 'Arjun Varma', 'subtotal': 3285.71, 'cgst': 82.14, 'sgst': 82.14, 'grand_total': 3450.00, 'payment_mode': 'Card (POS)', 'status': 'paid'},
        {'inv_num': 'INV-892399', 'date': '09/09/2026, 14:05', 'table': 'Takeaway #14', 'customer': 'Karthik Kumar', 'subtotal': 800.00, 'cgst': 20.00, 'sgst': 20.00, 'grand_total': 840.00, 'payment_mode': 'Cash', 'status': 'paid'},
        {'inv_num': 'INV-892398', 'date': '09/09/2026, 13:52', 'table': 'Zomato #4890', 'customer': 'Pooja Hegde', 'subtotal': 1123.81, 'cgst': 28.10, 'sgst': 28.10, 'grand_total': 1180.00, 'payment_mode': 'UPI', 'status': 'paid'},
        {'inv_num': 'INV-892397', 'date': '09/09/2026, 13:30', 'table': 'PDR-1', 'customer': 'Infosys Corp Team', 'subtotal': 8476.19, 'cgst': 211.90, 'sgst': 211.90, 'grand_total': 8900.00, 'payment_mode': 'Corporate Card', 'status': 'paid'},
    ]
    context = {
        'page_title': 'Indian GST Tax Invoices',
        'invoices': invoices_list
    }
    return render(request, 'billing/invoices.html', context)

def day_end_zreport(request):
    """
    Day-End Shift Closing Z-Report & Cash Drawer Balancing.
    """
    z_data = {
        'report_num': 'ZR-2026-0909-IND',
        'branch': 'Indiranagar Main (Bangalore)',
        'date': '09/09/2026',
        'shift': 'Afternoon Lunch Shift (11:00 AM - 16:00 PM)',
        'cashier': 'Sneha Reddy',
        'manager_on_duty': 'Pavan Kumar Varma',
        'gross_sales': 84250.00,
        'taxable_sales': 80238.10,
        'cgst_collected': 2005.95,
        'sgst_collected': 2005.95,
        'discounts_given': 1420.00,
        'covers_served': 184,
        'bills_count': 68,
        'tender_breakdown': [
            {'tender': 'UPI (PhonePe / GPay / Paytm QR)', 'amount': 58400.00, 'pct': '69.3%'},
            {'tender': 'Credit & Debit Cards (PineLabs / MSwipe)', 'amount': 18250.00, 'pct': '21.7%'},
            {'tender': 'Cash in Register', 'amount': 7600.00, 'pct': '9.0%'},
        ],
        'cash_reconciliation': {
            'opening_float': 5000.00,
            'cash_sales': 7600.00,
            'petty_cash_expenses': 850.00,
            'expected_in_drawer': 11750.00,
            'actual_counted': 11750.00,
            'variance': 0.00
        }
    }
    context = {
        'page_title': 'Day-End Closing Z-Report',
        'z': z_data
    }
    return render(request, 'billing/day_end_zreport.html', context)
