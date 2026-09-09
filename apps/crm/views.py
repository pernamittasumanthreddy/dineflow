from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['owner', 'manager', 'super_admin'])
def customer_list(request):
    """
    Customer Relationship Management (CRM) Directory.
    """
    customers = [
        {'id': 'CUST-1001', 'name': 'Dr. Anjali Sharma', 'phone': '+91 98490 12345', 'email': 'anjali.sharma@apollo.com', 'visits': 18, 'total_spent': 42800.00, 'tier': 'Gold VIP', 'fav_dish': 'Hyderabadi Chicken Biryani', 'status': 'active'},
        {'id': 'CUST-1002', 'name': 'Arjun Varma', 'phone': '+91 98200 67890', 'email': 'arjun.varma@tcs.com', 'visits': 12, 'total_spent': 26400.00, 'tier': 'Silver Club', 'fav_dish': 'Paneer Butter Masala', 'status': 'active'},
        {'id': 'CUST-1003', 'name': 'Pooja Hegde', 'phone': '+91 97110 44332', 'email': 'pooja.h@wipro.com', 'visits': 8, 'total_spent': 14900.00, 'tier': 'Silver Club', 'fav_dish': 'Royal Veg Dum Biryani', 'status': 'active'},
        {'id': 'CUST-1004', 'name': 'Vikram Rathore', 'phone': '+91 99000 88776', 'email': 'vikram.r@accenture.com', 'visits': 24, 'total_spent': 68200.00, 'tier': 'Platinum Executive', 'fav_dish': 'Mutton Handi Biryani', 'status': 'active'},
    ]
    context = {
        'page_title': 'Customer CRM Directory',
        'customers': customers
    }
    return render(request, 'crm/customer_list.html', context)

@role_required(['customer', 'owner', 'manager', 'cashier', 'super_admin'])
def loyalty_points(request):
    """
    DineClub Loyalty Points & Rewards System.
    """
    loyalty_members = [
        {'member_id': 'MEM-401', 'name': 'Vikram Rathore', 'tier': 'Platinum Executive', 'points_balance': 4850, 'points_value': 485.00, 'lifetime_earned': 12400, 'status': 'active'},
        {'member_id': 'MEM-402', 'name': 'Dr. Anjali Sharma', 'tier': 'Gold VIP', 'points_balance': 2450, 'points_value': 245.00, 'lifetime_earned': 7800, 'status': 'active'},
        {'member_id': 'MEM-403', 'name': 'Arjun Varma', 'tier': 'Silver Club', 'points_balance': 1120, 'points_value': 112.00, 'lifetime_earned': 3400, 'status': 'active'},
    ]
    context = {
        'page_title': 'DineClub Loyalty & Rewards',
        'members': loyalty_members
    }
    return render(request, 'crm/loyalty_points.html', context)

@role_required(['customer', 'owner', 'manager', 'cashier', 'super_admin'])
def offers_coupons(request):
    """
    Promotions, Happy Hours & Coupon Rules.
    """
    offers = [
        {'code': 'BIRYANI150', 'title': 'Flat ₹150 Off Biryani Handis', 'type': 'Flat Discount', 'min_bill': 600.00, 'valid_until': '30/09/2026', 'usage_count': 148, 'status': 'active'},
        {'code': 'SWEETGOLD', 'title': 'Complimentary Dessert on ₹1000+', 'type': 'Free Item Voucher', 'min_bill': 1000.00, 'valid_until': '31/10/2026', 'usage_count': 92, 'status': 'active'},
        {'code': 'CORP10', 'title': 'Corporate 10% Dining Privilege', 'type': 'Percentage Off', 'min_bill': 1500.00, 'valid_until': '31/12/2026', 'usage_count': 312, 'status': 'active'},
    ]
    context = {
        'page_title': 'Offers & Promo Coupons',
        'offers': offers
    }
    return render(request, 'crm/offers_coupons.html', context)

@role_required(['customer', 'waiter', 'manager', 'owner', 'super_admin'])
def reviews_feedback(request):
    """
    Table QR Feedback, Ratings & Sentiment Analysis.
    """
    reviews = [
        {'id': 'REV-901', 'guest': 'Dr. Anjali Sharma', 'table': 'T-04', 'rating': 5, 'food': 5, 'service': 5, 'ambiance': 5, 'comment': 'The Chicken Dum Biryani was phenomenal and aromatic. Service by Ravi Teja was top notch!', 'date': 'Today, 14:45'},
        {'id': 'REV-902', 'guest': 'Karthik Kumar', 'table': 'Takeaway', 'rating': 4, 'food': 4, 'service': 4, 'ambiance': 4, 'comment': 'Food quality was great, packaging was leakproof. Took 15 mins for pickup.', 'date': 'Today, 14:15'},
        {'id': 'REV-903', 'guest': 'Vikram Rathore', 'table': 'PDR-1', 'rating': 5, 'food': 5, 'service': 5, 'ambiance': 5, 'comment': 'Best Mutton Biryani in Indiranagar. Excellent hospitality for our client meeting.', 'date': 'Yesterday'},
    ]
    context = {
        'page_title': 'Customer Reviews & Feedback',
        'reviews': reviews
    }
    return render(request, 'crm/reviews_feedback.html', context)
