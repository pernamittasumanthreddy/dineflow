"""Global System Settings and Hardware Preferences Views."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.settings_manager.models import SystemSetting
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('settings')
def settings_overview_view(request):
    """Configuration panel for restaurant global settings and thermal printer hardware."""
    settings_qs = SystemSetting.objects.all()
    
    if not settings_qs.exists():
        SystemSetting.objects.create(key='THERMAL_PRINTER_WIDTH_MM', value='80', description='POS Thermal receipt roll width (58mm or 80mm)')
        SystemSetting.objects.create(key='AUTO_PRINT_KOT_ON_ORDER', value='True', description='Automatically fire KOT print on order placement')
        SystemSetting.objects.create(key='ALLOW_CUSTOMER_FEEDBACK', value='True', description='Enable post-dining QR review collection')
        SystemSetting.objects.create(key='DEFAULT_TABLE_TURNOVER_TARGET_MINS', value='60', description='Target dining duration per table')
        settings_qs = SystemSetting.objects.all()

    if request.method == 'POST':
        for setting in settings_qs:
            val = request.POST.get(setting.key)
            if val is not None:
                setting.value = val.strip()
                setting.save()
        messages.success(request, "System settings updated successfully.")
        return redirect('settings_manager:overview')

    return render(request, 'settings_manager/settings_overview.html', {'settings': settings_qs})
