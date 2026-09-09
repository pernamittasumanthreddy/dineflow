"""Tax Management Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.tax.models import TaxCategory
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('settings')
def tax_category_list_view(request):
    """View and update Indian GST slabs and SAC codes."""
    categories = TaxCategory.objects.all()
    if not categories.exists():
        TaxCategory.objects.create(name='Standard Restaurant Food', sac_code='996331', total_rate_percent=5.00, cgst_rate_percent=2.50, sgst_rate_percent=2.50)
        TaxCategory.objects.create(name='Beverages / Mocktails', sac_code='996332', total_rate_percent=12.00, cgst_rate_percent=6.00, sgst_rate_percent=6.00)
        TaxCategory.objects.create(name='Exempt Items', sac_code='996339', total_rate_percent=0.00, cgst_rate_percent=0.00, sgst_rate_percent=0.00)
        categories = TaxCategory.objects.all()

    return render(request, 'tax/tax_list.html', {'categories': categories})
