from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['super_admin'])
def super_admin_dashboard(request):
    """Role 1: Super Admin (SaaS Multi-Tenant Management)"""
    context = {
        'page_title': 'Super Admin SaaS Command Center',
        'kpis': [
            {'label': 'Total Restaurant Chains', 'value': '142', 'trend': '+8%', 'trend_up': True, 'icon': 'df-icon-maroon', 'emoji': '🏢'},
            {'label': 'Active Outlets / Branches', 'value': '486', 'trend': '+14%', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '📍'},
            {'label': 'Monthly Recurring Rev (MRR)', 'value': '₹24,80,000', 'trend': '+18.5%', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '💰'},
            {'label': 'System Health & SLA', 'value': '99.99%', 'trend': 'Optimal', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '⚡'},
        ],
        'tenants': [
            {'name': 'Andhra Spice Kitchen (Flagship)', 'branches': 5, 'city': 'Bangalore/Hyderabad', 'plan': 'Multi-Chain Enterprise', 'status': 'active', 'mrr': '₹29,995'},
            {'name': 'Coastal Curry House & Tiffin', 'branches': 3, 'city': 'Chennai', 'plan': 'Multi-Chain Enterprise', 'status': 'active', 'mrr': '₹17,997'},
            {'name': 'Vijayawada Food Court', 'branches': 2, 'city': 'Vijayawada', 'plan': 'Single Outlet Pro', 'status': 'active', 'mrr': '₹4,998'},
            {'name': 'Hyderabad Biryani Hub', 'branches': 8, 'city': 'Hyderabad', 'plan': 'Cloud Kitchen Network', 'status': 'active', 'mrr': '₹35,992'},
            {'name': 'Kerala Taste Traditional', 'branches': 1, 'city': 'Kochi', 'plan': 'Single Outlet Pro', 'status': 'active', 'mrr': '₹2,499'},
        ]
    }
    return render(request, 'dashboard/super_admin.html', context)

@role_required(['owner', 'super_admin'])
def owner_dashboard(request):
    """Role 2: Restaurant Owner (Executive Chain Financials)"""
    context = {
        'page_title': 'Executive Command Dashboard',
        'kpis': [
            {'label': "Today's Gross Sales", 'value': '₹1,48,650', 'trend': '+14.2% vs yesterday', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '💵'},
            {'label': 'Total Orders Served', 'value': '342', 'trend': '+28 orders', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '🍽️'},
            {'label': 'Average Order Value (AOV)', 'value': '₹434.60', 'trend': '+₹24.00', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '📈'},
            {'label': 'Estimated Net Profit (Today)', 'value': '₹56,400', 'trend': '37.9% Margin', 'trend_up': True, 'icon': 'df-icon-maroon', 'emoji': '💎'},
        ],
        'branch_performance': [
            {'branch': 'Indiranagar Main (Bangalore)', 'sales': '₹58,400', 'orders': 124, 'aov': '₹470', 'turnover': '42 mins', 'status': 'Peak Service'},
            {'branch': 'Banjara Hills Flagship (Hyderabad)', 'sales': '₹49,250', 'orders': 108, 'aov': '₹456', 'turnover': '38 mins', 'status': 'High Demand'},
            {'branch': 'Connaught Place (New Delhi)', 'sales': '₹24,100', 'orders': 62, 'aov': '₹388', 'turnover': '46 mins', 'status': 'Moderate'},
            {'branch': 'Anna Nagar (Chennai)', 'sales': '₹16,900', 'orders': 48, 'aov': '₹352', 'turnover': '34 mins', 'status': 'Normal'},
        ],
        'top_dishes': [
            {'name': 'Hyderabadi Chicken Dum Biryani', 'category': 'Biryani', 'sold': 142, 'revenue': '₹48,280', 'margin': '64%', 'diet': 'nonveg'},
            {'name': 'Paneer Butter Masala', 'category': 'Curries', 'sold': 84, 'revenue': '₹21,840', 'margin': '68%', 'diet': 'veg'},
            {'name': 'Butter Garlic Naan', 'category': 'Breads', 'sold': 210, 'revenue': '₹13,650', 'margin': '82%', 'diet': 'veg'},
            {'name': 'Murg Malai Tikka (8 pcs)', 'category': 'Tandoor', 'sold': 56, 'revenue': '₹19,040', 'margin': '61%', 'diet': 'nonveg'},
        ]
    }
    return render(request, 'dashboard/owner.html', context)

@role_required(['manager', 'owner', 'super_admin'])
def manager_dashboard(request):
    """Role 3: Restaurant Manager (Floor Operations & Handovers)"""
    context = {
        'page_title': 'General Manager Floor Operations',
        'kpis': [
            {'label': 'Live Table Occupancy', 'value': '22 / 28', 'trend': '78.5% Occupied', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '🪑'},
            {'label': 'Active KOTs in Kitchen', 'value': '14', 'trend': '2 Overdue (>15m)', 'trend_up': False, 'icon': 'df-icon-maroon', 'emoji': '🔥'},
            {'label': 'Staff On Duty (Floor/Kitchen)', 'value': '18 / 20', 'trend': '2 On Leave', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '👥'},
            {'label': 'Dinner Reservations Today', 'value': '16 Tables', 'trend': '6 VIP Parties', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '📅'},
        ],
        'live_tables': [
            {'table': 'T-04 (AC Hall)', 'waiter': 'Ravi Teja', 'guests': 4, 'occupied_since': '38 mins', 'amount': '₹2,450', 'status': 'Dining'},
            {'table': 'T-08 (Terrace)', 'waiter': 'Arjun Varma', 'guests': 6, 'occupied_since': '18 mins', 'amount': '₹3,120', 'status': 'Food Served'},
            {'table': 'T-12 (PDR-1)', 'waiter': 'Sneha Reddy', 'guests': 8, 'occupied_since': '55 mins', 'amount': '₹6,800', 'status': 'Dessert / Bill'},
            {'table': 'TR-02 (Terrace)', 'waiter': 'Pavan V', 'guests': 2, 'occupied_since': '12 mins', 'amount': '₹890', 'status': 'Starters'},
        ]
    }
    return render(request, 'dashboard/manager.html', context)

@role_required(['kitchen', 'manager', 'owner', 'super_admin'])
def kitchen_dashboard(request):
    """Role 4: Kitchen Staff / Chef (KDS Station Manager)"""
    context = {
        'page_title': 'Kitchen Display & Chef Station',
        'kpis': [
            {'label': 'New Unassigned Tickets', 'value': '4 KOTs', 'trend': 'Needs Attention', 'trend_up': False, 'icon': 'df-icon-saffron', 'emoji': '🔔'},
            {'label': 'Tickets on Flame (Cooking)', 'value': '8 KOTs', 'trend': 'Avg Prep: 11.4m', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '👨‍🍳'},
            {'label': 'Plated & Ready to Serve', 'value': '5 KOTs', 'trend': 'Call Runner', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '✅'},
            {'label': 'Completed Today', 'value': '214 KOTs', 'trend': 'Peak Speed', 'trend_up': True, 'icon': 'df-icon-charcoal', 'emoji': '🚀'},
        ]
    }
    return render(request, 'dashboard/kitchen.html', context)

@role_required(['waiter', 'manager', 'owner', 'super_admin'])
def waiter_dashboard(request):
    """Role 5: Waiter / Captain (Captain Terminal & Tables)"""
    context = {
        'page_title': 'Captain Ordering Terminal',
        'kpis': [
            {'label': 'My Assigned Tables', 'value': '6 Tables', 'trend': 'Section: AC Dining', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '🪑'},
            {'label': 'Active Running Orders', 'value': '4 Orders', 'trend': '₹8,920 Total', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '📝'},
            {'label': 'Orders Ready for Pickup', 'value': '2 Ready', 'trend': 'Table T-02 & T-05', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '🍲'},
            {'label': 'My Tips Earned Today', 'value': '₹1,240', 'trend': 'UPI & Cash Tips', 'trend_up': True, 'icon': 'df-icon-gold', 'emoji': '💸'},
        ]
    }
    return render(request, 'dashboard/waiter.html', context)

@role_required(['cashier', 'manager', 'owner', 'super_admin'])
def cashier_dashboard(request):
    """Role 6: Cashier (Billing, Settlement & Cash Balancing)"""
    context = {
        'page_title': 'Cashier Terminal & GST Settlement',
        'kpis': [
            {'label': "Today's Total Collection", 'value': '₹1,48,650', 'trend': 'Shift 1 & 2', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '💵'},
            {'label': 'UPI Collection (QR/Net)', 'value': '₹1,02,400', 'trend': '68.9% of Total', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '📱'},
            {'label': 'Card Swipe Collection', 'value': '₹32,150', 'trend': '21.6% of Total', 'trend_up': True, 'icon': 'df-icon-maroon', 'emoji': '💳'},
            {'label': 'Cash in Register Drawer', 'value': '₹14,100', 'trend': 'Float: ₹5,000', 'trend_up': True, 'icon': 'df-icon-gold', 'emoji': '🪙'},
        ],
        'recent_bills': [
            {'inv': 'INV-892401', 'table': 'T-04', 'time': '14:32', 'amount': '₹1,260.00', 'mode': 'UPI', 'status': 'paid'},
            {'inv': 'INV-892400', 'table': 'T-08', 'time': '14:18', 'amount': '₹3,450.00', 'mode': 'Card', 'status': 'paid'},
            {'inv': 'INV-892399', 'table': 'Takeaway #14', 'time': '14:05', 'amount': '₹840.00', 'mode': 'Cash', 'status': 'paid'},
            {'inv': 'INV-892398', 'table': 'Zomato #4890', 'time': '13:52', 'amount': '₹1,180.00', 'mode': 'UPI', 'status': 'paid'},
        ]
    }
    return render(request, 'dashboard/cashier.html', context)

@role_required(['inventory', 'manager', 'owner', 'super_admin'])
def inventory_dashboard(request):
    """Role 7: Inventory Manager (Stock, POs & Waste)"""
    context = {
        'page_title': 'Raw Materials & Stock Control',
        'kpis': [
            {'label': 'Total Tracked SKUs', 'value': '184 Items', 'trend': '₹4,12,000 Value', 'trend_up': True, 'icon': 'df-icon-charcoal', 'emoji': '📦'},
            {'label': 'Low Stock Critical Alerts', 'value': '6 Items', 'trend': 'Below Buffer Safety', 'trend_up': False, 'icon': 'df-icon-danger', 'emoji': '⚠️'},
            {'label': 'Pending Purchase Orders', 'value': '3 Orders', 'trend': '₹64,500 Inwarding', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '📝'},
            {'label': 'Waste & Spoilage Today', 'value': '₹1,450', 'trend': '0.98% of COGS', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '🗑️'},
        ],
        'low_stock_items': [
            {'item': 'India Gate Classic Basmati Rice', 'current': '12.5 kg', 'min': '30.0 kg', 'unit': 'kg', 'status': 'low_stock', 'supplier': 'Sri Balaji Agro'},
            {'item': 'Fresh Malai Paneer Block', 'current': '4.2 kg', 'min': '15.0 kg', 'unit': 'kg', 'status': 'low_stock', 'supplier': 'Heritage Dairy'},
            {'item': 'Pure Desi Cow Ghee (Tin)', 'current': '3.0 L', 'min': '10.0 L', 'unit': 'L', 'status': 'low_stock', 'supplier': 'Amul India'},
            {'item': 'Kashmiri Red Chili Powder', 'current': '1.8 kg', 'min': '5.0 kg', 'unit': 'kg', 'status': 'low_stock', 'supplier': 'MDH Spices Hub'},
        ]
    }
    return render(request, 'dashboard/inventory.html', context)

@role_required(['hr', 'owner', 'super_admin'])
def hr_dashboard(request):
    """Role 8: HR Manager (Staff, Attendance & Payroll)"""
    context = {
        'page_title': 'Human Resources & Payroll Command',
        'kpis': [
            {'label': 'Total Active Staff', 'value': '42 Staff', 'trend': '4 Branches', 'trend_up': True, 'icon': 'df-icon-charcoal', 'emoji': '👥'},
            {'label': 'Present Today (Biometric)', 'value': '38 Present', 'trend': '90.5% Attendance', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '⏱️'},
            {'label': 'Staff on Approved Leave', 'value': '4 On Leave', 'trend': '2 Planned Off', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '🏖️'},
            {'label': 'Monthly Payroll Estimate', 'value': '₹8,45,000', 'trend': 'Inc. PF / ESI / TDS', 'trend_up': True, 'icon': 'df-icon-maroon', 'emoji': '💰'},
        ],
        'staff_attendance': [
            {'name': 'Ravi Teja', 'role': 'Head Captain (Waiter)', 'shift': 'Morning (10:00 - 18:00)', 'punch_in': '09:52 AM', 'status': 'present'},
            {'name': 'Chef Sanjeev Teja', 'role': 'Executive Chef', 'shift': 'Split (11:00 - 23:00)', 'punch_in': '10:45 AM', 'status': 'present'},
            {'name': 'Sneha Reddy', 'role': 'Cashier & Billing', 'shift': 'Evening (16:00 - 00:00)', 'punch_in': '-', 'status': 'pending'},
            {'name': 'Arjun Varma', 'role': 'Captain (Service)', 'shift': 'Morning (10:00 - 18:00)', 'punch_in': '10:14 AM', 'status': 'late'},
        ]
    }
    return render(request, 'dashboard/hr.html', context)

@role_required(['customer', 'owner', 'super_admin'])
def customer_dashboard(request):
    """Role 9: Customer Portal (Menu, Bookings & Rewards)"""
    context = {
        'page_title': 'Guest Experience & DineClub Rewards',
        'kpis': [
            {'label': 'DineClub Loyalty Points', 'value': '2,450 Pts', 'trend': 'Worth ₹245.00', 'trend_up': True, 'icon': 'df-icon-gold', 'emoji': '🎁'},
            {'label': 'Membership Tier', 'value': 'Gold VIP', 'trend': '10% Cashback on Dine-In', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '👑'},
            {'label': 'Total Visits to Chain', 'value': '18 Visits', 'trend': 'Fav: Indiranagar', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '🍽️'},
            {'label': 'Available Promo Vouchers', 'value': '3 Coupons', 'trend': 'Flat ₹150 Off Biryani', 'trend_up': True, 'icon': 'df-icon-maroon', 'emoji': '🎟️'},
        ]
    }
    return render(request, 'dashboard/customer.html', context)

@role_required(['analytics', 'owner', 'super_admin'])
def analytics_dashboard(request):
    """Role 10: Analytics & BI (Multi-Branch Intelligence & AI Forecast)"""
    context = {
        'page_title': 'Business Intelligence & AI Demand Center',
        'kpis': [
            {'label': 'Current Month Revenue', 'value': '₹38,40,250', 'trend': '+16.8% vs last mo', 'trend_up': True, 'icon': 'df-icon-green', 'emoji': '📈'},
            {'label': 'Total Monthly Covers', 'value': '9,240 Guests', 'trend': '+1,120 YoY', 'trend_up': True, 'icon': 'df-icon-terracotta', 'emoji': '👥'},
            {'label': 'Food Cost Ratio (COGS)', 'value': '28.4%', 'trend': 'Target: < 30%', 'trend_up': True, 'icon': 'df-icon-saffron', 'emoji': '🍲'},
            {'label': 'AI Predicted Weekend Rush', 'value': '+42% Footfall', 'trend': 'Prep 220kg Biryani Rice', 'trend_up': True, 'icon': 'df-icon-maroon', 'emoji': '🧠'},
        ]
    }
    return render(request, 'dashboard/analytics.html', context)
