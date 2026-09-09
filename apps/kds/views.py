from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['kitchen', 'manager', 'owner', 'super_admin'])
def live_kds(request):
    """
    Dedicated Fullscreen Kitchen Display System (KDS) View.
    """
    context = {
        'page_title': 'Kitchen Display System (KDS)',
    }
    return render(request, 'kds/live.html', context)
