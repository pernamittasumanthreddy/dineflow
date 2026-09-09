from django.shortcuts import render

def floor_plan(request):
    """
    Visual Table Layout & Floor Plan Management.
    """
    context = {
        'page_title': 'Interactive Floor Plan & Table Management',
    }
    return render(request, 'tables/floor_plan.html', context)

def reservations(request):
    """
    Table Reservations & Guest Waitlist Management.
    """
    reservations_list = [
        {'id': 'RES-1081', 'guest': 'Dr. Anjali Sharma', 'phone': '+91 98490 12345', 'party_size': 8, 'zone': 'PDR-1', 'time': '08:30 PM', 'date': 'Today', 'status': 'confirmed', 'notes': 'Doctor Birthday party, floral center'},
        {'id': 'RES-1082', 'guest': 'Mr. Arjun Varma', 'phone': '+91 98200 67890', 'party_size': 4, 'zone': 'Open Terrace', 'time': '09:00 PM', 'date': 'Today', 'status': 'confirmed', 'notes': 'Candle light setup'},
        {'id': 'RES-1083', 'guest': 'Infosys Tech Leadership', 'phone': '+91 99887 11223', 'party_size': 16, 'zone': 'PDR-2', 'time': '07:45 PM', 'date': 'Today', 'status': 'confirmed', 'notes': 'Corporate billing GST invoice'},
        {'id': 'RES-1084', 'guest': 'Ravi Teja & Family', 'phone': '+91 97000 55443', 'party_size': 6, 'zone': 'AC Dining', 'time': '08:15 PM', 'date': 'Today', 'status': 'pending', 'notes': 'High chair required for toddler'},
    ]
    context = {
        'page_title': 'Table Reservations & Guest Waitlist',
        'reservations': reservations_list
    }
    return render(request, 'tables/reservations.html', context)
