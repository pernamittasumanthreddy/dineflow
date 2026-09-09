from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['owner', 'cashier', 'super_admin'])
def gst_slabs(request):
    """
    Indian GST Rates, SAC Slabs & Tax Configurations.
    """
    tax_rules = [
        {'code': 'SAC-996331', 'description': 'Restaurant Dining (AC & Non-AC) - Food & Soft Beverages', 'cgst': '2.5%', 'sgst': '2.5%', 'igst': '5.0%', 'itc_eligibility': 'No Input Tax Credit (Standard)', 'status': 'active'},
        {'code': 'SAC-996332', 'description': 'Takeaway & Cloud Kitchen Direct Online Delivery', 'cgst': '2.5%', 'sgst': '2.5%', 'igst': '5.0%', 'itc_eligibility': 'No Input Tax Credit', 'status': 'active'},
        {'code': 'SAC-996333', 'description': 'Outdoor Catering & Banquet Hall Service', 'cgst': '9.0%', 'sgst': '9.0%', 'igst': '18.0%', 'itc_eligibility': 'Eligible with Full ITC', 'status': 'active'},
        {'code': 'SAC-996334', 'description': 'Alcoholic Beverages Served with Food (State Excise)', 'cgst': 'State VAT', 'sgst': 'State VAT', 'igst': 'Excise', 'itc_eligibility': 'State Specific VAT Rules', 'status': 'active'},
        {'code': 'SAC-996335', 'description': 'Exempted Raw Groceries & Farm Fresh Produce', 'cgst': '0.0%', 'sgst': '0.0%', 'igst': '0.0%', 'itc_eligibility': 'Exempt Category', 'status': 'active'},
    ]
    context = {
        'page_title': 'Indian GST Rates & SAC Codes',
        'tax_rules': tax_rules
    }
    return render(request, 'tax_mgmt/gst_slabs.html', context)
