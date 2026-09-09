from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['waiter', 'kitchen', 'manager', 'cashier', 'owner', 'customer', 'super_admin'])
def live_orders(request):
    """
    Omnichannel Order Management (Dine-in, Takeaway, Delivery, Swiggy, Zomato).
    """
    orders_list = [
        {'id': 'ORD-892410', 'channel': 'Dine-In', 'table': 'T-04 (AC)', 'customer': 'Dr. Anjali Sharma', 'items_summary': 'Chicken Biryani (2), Paneer Butter Masala (1), Naan (4)', 'amount': 1260.00, 'time': '14:32 (12m ago)', 'payment_status': 'paid', 'order_status': 'preparing'},
        {'id': 'ORD-892409', 'channel': 'Zomato', 'table': 'Rider #892', 'customer': 'Vikram Rathore', 'items_summary': 'Mutton Handi Biryani (1), Mirchi Salan (1)', 'amount': 540.00, 'time': '14:28 (16m ago)', 'payment_status': 'paid', 'order_status': 'ready'},
        {'id': 'ORD-892408', 'channel': 'Dine-In', 'table': 'T-08 (Terrace)', 'customer': 'Arjun Varma', 'items_summary': 'Chicken 65 (2), Butter Roti (6), Dal Makhani (1)', 'amount': 980.00, 'time': '14:20 (24m ago)', 'payment_status': 'pending', 'order_status': 'served'},
        {'id': 'ORD-892407', 'channel': 'Swiggy', 'table': 'Rider #412', 'customer': 'Pooja Hegde', 'items_summary': 'Royal Veg Dum Biryani (2), Gulab Jamun (2)', 'amount': 760.00, 'time': '14:15 (29m ago)', 'payment_status': 'paid', 'order_status': 'delivered'},
        {'id': 'ORD-892406', 'channel': 'Takeaway', 'table': 'Counter #1', 'customer': 'Karthik Kumar', 'items_summary': 'Chicken Tikka (1), Naan (2)', 'amount': 470.00, 'time': '14:05 (39m ago)', 'payment_status': 'paid', 'order_status': 'completed'},
    ]
    context = {
        'page_title': 'Omnichannel Live Orders',
        'orders': orders_list
    }
    return render(request, 'orders/live_orders.html', context)
