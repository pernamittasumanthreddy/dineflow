from django.shortcuts import render

def fleet(request):
    """
    In-House Delivery Fleet & Rider Dispatcher.
    """
    riders = [
        {'id': 'RDR-01', 'name': 'Kiran Varma', 'mobile': '+91 98490 33441', 'bike_number': 'TS 09 EA 4512', 'active_orders': 2, 'deliveries_today': 14, 'earnings': 840.00, 'status': 'on_delivery'},
        {'id': 'RDR-02', 'name': 'Manoj Kumar', 'mobile': '+91 97000 88221', 'bike_number': 'TS 09 EB 8921', 'active_orders': 0, 'deliveries_today': 16, 'earnings': 960.00, 'status': 'available'},
        {'id': 'RDR-03', 'name': 'Shiva Prasad', 'mobile': '+91 99887 55443', 'bike_number': 'TS 09 EC 3419', 'active_orders': 1, 'deliveries_today': 11, 'earnings': 660.00, 'status': 'on_delivery'},
    ]
    context = {
        'page_title': 'Delivery Fleet & Riders',
        'riders': riders
    }
    return render(request, 'delivery/fleet.html', context)
