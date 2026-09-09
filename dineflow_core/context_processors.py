"""
DineFlow - Global Context Processors
Provides system-wide metadata, multi-role switching, active branch context,
Indian currency formatting, GST rates, and notification badges across all templates.
"""

def dineflow_global_context(request):
    # Simulated active role stored in session (default: 'owner')
    current_role = request.session.get('dineflow_active_role', 'owner')
    active_branch = request.session.get('dineflow_active_branch', 'Indiranagar Main (Bangalore)')
    
    roles = [
        {
            'key': 'super_admin',
            'name': 'Super Admin',
            'icon': 'shield-lock',
            'desc': 'Multi-Tenant & System Administration',
            'badge': 'SaaS Root'
        },
        {
            'key': 'owner',
            'name': 'Restaurant Owner',
            'icon': 'briefcase',
            'desc': 'Chain Executive & Financials',
            'badge': 'Executive'
        },
        {
            'key': 'manager',
            'name': 'Restaurant Manager',
            'icon': 'people',
            'desc': 'Daily Shift & Floor Operations',
            'badge': 'Operations'
        },
        {
            'key': 'kitchen',
            'name': 'Kitchen Staff / Chef',
            'icon': 'fire',
            'desc': 'KDS & Prep Queue Management',
            'badge': 'Live KDS'
        },
        {
            'key': 'waiter',
            'name': 'Waiter / Captain',
            'icon': 'cup-hot',
            'desc': 'Table Ordering & Service',
            'badge': 'POS Captain'
        },
        {
            'key': 'cashier',
            'name': 'Cashier',
            'icon': 'cash-stack',
            'desc': 'POS Settlement & GST Billing',
            'badge': 'Billing'
        },
        {
            'key': 'inventory',
            'name': 'Inventory Manager',
            'icon': 'box-seam',
            'desc': 'Raw Materials, Stock & POs',
            'badge': 'Stock'
        },
        {
            'key': 'hr',
            'name': 'HR Manager',
            'icon': 'person-badge',
            'desc': 'Attendance, Shifts & Payroll',
            'badge': 'HRMS'
        },
        {
            'key': 'customer',
            'name': 'Customer',
            'icon': 'emoji-smile',
            'desc': 'Digital Menu, Bookings & Rewards',
            'badge': 'Guest'
        },
        {
            'key': 'analytics',
            'name': 'Analytics & BI',
            'icon': 'graph-up-arrow',
            'desc': 'Business Intelligence & AI Forecast',
            'badge': 'BI Insights'
        },
    ]
    
    branches = [
        {'id': 1, 'name': 'Indiranagar Main (Bangalore)', 'city': 'Bangalore', 'gstin': '29AABCS1429B1Z5', 'tables': 28, 'fssai': '11223334000121'},
        {'id': 2, 'name': 'Banjara Hills Flagship (Hyderabad)', 'city': 'Hyderabad', 'gstin': '36AABCS1429B1Z8', 'tables': 36, 'fssai': '13622014000889'},
        {'id': 3, 'name': 'Connaught Place (New Delhi)', 'city': 'New Delhi', 'gstin': '07AABCS1429B1Z2', 'tables': 24, 'fssai': '10721008000456'},
        {'id': 4, 'name': 'Anna Nagar Central (Chennai)', 'city': 'Chennai', 'gstin': '33AABCS1429B1Z4', 'tables': 30, 'fssai': '13320015000782'},
        {'id': 5, 'name': 'Hitec City Cloud Kitchen (Hyderabad)', 'city': 'Hyderabad', 'gstin': '36AABCS1429B1Z8', 'tables': 0, 'fssai': '13623019000341'},
    ]

    current_user_profile = {
        'name': 'Pavan Kumar Varma',
        'email': 'pavan.varma@dineflow.in',
        'phone': '+91 98490 12345',
        'role_title': next((r['name'] for r in roles if r['key'] == current_role), 'Restaurant Owner'),
        'role_key': current_role,
        'avatar_initials': 'PK',
        'branch': active_branch,
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
        'version': 'v4.8.0 Enterprise'
    }

    pending_notifications = [
        {'id': 1, 'type': 'warning', 'title': 'Low Stock Alert', 'text': 'Basmati Rice stock is below 15 kg in Banjara Hills store.', 'time': '5 min ago', 'icon': 'exclamation-triangle'},
        {'id': 2, 'type': 'danger', 'title': 'KDS Bottleneck', 'text': 'Table T-08 Order (KOT #1042) exceeding prep target (28m elapsed).', 'time': '12 min ago', 'icon': 'fire'},
        {'id': 3, 'type': 'success', 'title': 'Z-Report Generated', 'text': 'Indiranagar afternoon shift closed: ₹84,250 collected (UPI: 68%).', 'time': '34 min ago', 'icon': 'check-circle'},
        {'id': 4, 'type': 'info', 'title': 'New VIP Reservation', 'text': 'Dr. Anjali Sharma booked PDR-1 for 8 guests today at 8:30 PM.', 'time': '1 hr ago', 'icon': 'calendar-check'},
    ]

    return {
        'CURRENT_ROLE': current_role,
        'ALL_ROLES': roles,
        'BRANCHES': branches,
        'ACTIVE_BRANCH': active_branch,
        'CURRENT_USER': current_user_profile,
        'RESTAURANT_INFO': restaurant_info,
        'NOTIFICATIONS': pending_notifications,
        'UNREAD_NOTIFICATIONS_COUNT': len(pending_notifications),
    }
