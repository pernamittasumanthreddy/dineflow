"""
DineFlow - Global Context Processors
Provides real authenticated user context, active branch, role metadata, and notifications.
"""
from apps.accounts.models import Role

def dineflow_global_context(request):
    user = getattr(request, 'user', None)
    
    current_role_code = 'owner'
    role_title = 'Restaurant Owner'
    user_name = 'Vikramaditya Rao'
    user_email = 'owner@dineflow.in'
    user_initials = 'VR'
    active_branch = request.session.get('dineflow_active_branch', 'Indiranagar Main (Bangalore)')
    employee_code = 'OWN-001'
    phone = '+91 98450 11002'

    if user and user.is_authenticated:
        try:
            profile = user.userprofile
            current_role_code = profile.role.code
            role_title = profile.role.name
            user_name = user.get_full_name() or user.username
            user_email = user.email
            user_initials = profile.avatar_initials or (user.first_name[:1] + user.last_name[:1] if user.last_name else user.username[:2]).upper()
            active_branch = profile.branch or active_branch
            employee_code = profile.employee_code
            phone = profile.phone
        except Exception:
            if user.is_superuser:
                current_role_code = 'super_admin'
                role_title = 'Super Admin'
                user_name = user.get_full_name() or user.username
                user_email = user.email
                user_initials = 'SA'

    branches = [
        {'id': 1, 'name': 'Indiranagar Main (Bangalore)', 'city': 'Bangalore', 'gstin': '29AABCS1429B1Z5', 'tables': 28, 'fssai': '11223334000121'},
        {'id': 2, 'name': 'Banjara Hills Flagship (Hyderabad)', 'city': 'Hyderabad', 'gstin': '36AABCS1429B1Z8', 'tables': 36, 'fssai': '13622014000889'},
        {'id': 3, 'name': 'Connaught Place (New Delhi)', 'city': 'New Delhi', 'gstin': '07AABCS1429B1Z2', 'tables': 24, 'fssai': '10721008000456'},
        {'id': 4, 'name': 'Anna Nagar Central (Chennai)', 'city': 'Chennai', 'gstin': '33AABCS1429B1Z4', 'tables': 30, 'fssai': '13320015000782'},
        {'id': 5, 'name': 'Hitec City Cloud Kitchen (Hyderabad)', 'city': 'Hyderabad', 'gstin': '36AABCS1429B1Z8', 'tables': 0, 'fssai': '13623019000341'},
    ]

    current_user_profile = {
        'name': user_name,
        'email': user_email,
        'phone': phone,
        'role_title': role_title,
        'role_key': current_role_code,
        'avatar_initials': user_initials,
        'branch': active_branch,
        'employee_code': employee_code,
    }

    restaurant_info = {
        'brand_name': 'Andhra Spice Kitchen & Grand Dine',
        'company_legal_name': 'DineFlow Hospitality Private Limited',
        'fssai_license': '10020042001234',
        'gstin': '36AABCS1429B1Z8',
        'currency_symbol': '₹',
        'currency_code': 'INR',
        'cgst_rate': 2.5,
        'sgst_rate': 2.5,
        'igst_rate': 5.0,
        'support_phone': '1800-425-3463',
        'support_email': 'support@dineflow.in',
        'version': 'v4.8.0 Enterprise RBAC'
    }

    pending_notifications = [
        {'id': 1, 'type': 'warning', 'title': 'Low Stock Alert', 'text': 'Basmati Rice stock is below 15 kg in Banjara Hills store.', 'time': '5 min ago', 'icon': 'exclamation-triangle'},
        {'id': 2, 'type': 'danger', 'title': 'KDS Bottleneck', 'text': 'Table T-08 Order (KOT #1042) exceeding prep target (28m elapsed).', 'time': '12 min ago', 'icon': 'fire'},
        {'id': 3, 'type': 'success', 'title': 'Z-Report Generated', 'text': 'Indiranagar afternoon shift closed: ₹84,250 collected (UPI: 68%).', 'time': '34 min ago', 'icon': 'check-circle'},
        {'id': 4, 'type': 'info', 'title': 'New VIP Reservation', 'text': 'Dr. Anjali Sharma booked PDR-1 for 8 guests today at 8:30 PM.', 'time': '1 hr ago', 'icon': 'calendar-check'},
    ]

    return {
        'CURRENT_ROLE': current_role_code,
        'USER_ROLE': current_role_code,
        'BRANCHES': branches,
        'ACTIVE_BRANCH': active_branch,
        'CURRENT_USER': current_user_profile,
        'RESTAURANT_INFO': restaurant_info,
        'NOTIFICATIONS': pending_notifications,
        'UNREAD_NOTIFICATIONS_COUNT': len(pending_notifications),
    }
