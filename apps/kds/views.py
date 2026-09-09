from django.shortcuts import render

def live_kds(request):
    """
    Dedicated Fullscreen Kitchen Display System (KDS) View.
    """
    context = {
        'page_title': 'Kitchen Display System (KDS)',
    }
    return render(request, 'kds/live.html', context)
