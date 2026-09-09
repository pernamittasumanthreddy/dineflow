from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['cashier', 'waiter', 'manager', 'owner', 'super_admin'])
def terminal(request):
    """
    High-Speed Touch POS Terminal for Waiters, Cashiers, and Managers.
    """
    categories = [
        {'key': 'all', 'name': 'All Items', 'icon': '🍽️'},
        {'key': 'biryani', 'name': 'Biryani & Rice', 'icon': '🍚'},
        {'key': 'tandoor', 'name': 'Tandoor Starters', 'icon': '🍢'},
        {'key': 'curries', 'name': 'Main Curries', 'icon': '🍲'},
        {'key': 'breads', 'name': 'Indian Breads', 'icon': '🫓'},
        {'key': 'south_indian', 'name': 'Tiffins & Meals', 'icon': '🥞'},
        {'key': 'desserts', 'name': 'Desserts', 'icon': '🍨'},
        {'key': 'beverages', 'name': 'Beverages', 'icon': '☕'},
    ]

    menu_items = [
        {'id': 101, 'name': 'Hyderabadi Chicken Dum Biryani', 'category': 'biryani', 'price': 340.00, 'diet': 'nonveg', 'prep_time': '12m'},
        {'id': 102, 'name': 'Special Mutton Handi Biryani', 'category': 'biryani', 'price': 460.00, 'diet': 'nonveg', 'prep_time': '15m'},
        {'id': 103, 'name': 'Royal Veg Dum Biryani', 'category': 'biryani', 'price': 240.00, 'diet': 'veg', 'prep_time': '10m'},
        {'id': 104, 'name': 'Andhra Spicy Chicken 65', 'category': 'tandoor', 'price': 280.00, 'diet': 'nonveg', 'prep_time': '10m'},
        {'id': 105, 'name': 'Murg Malai Tikka (8 pcs)', 'category': 'tandoor', 'price': 340.00, 'diet': 'nonveg', 'prep_time': '14m'},
        {'id': 106, 'name': 'Paneer Tikka Shashlik', 'category': 'tandoor', 'price': 290.00, 'diet': 'veg', 'prep_time': '12m'},
        {'id': 107, 'name': 'Paneer Butter Masala', 'category': 'curries', 'price': 260.00, 'diet': 'veg', 'prep_time': '10m'},
        {'id': 108, 'name': 'Dal Makhani Handi', 'category': 'curries', 'price': 220.00, 'diet': 'veg', 'prep_time': '8m'},
        {'id': 109, 'name': 'Chettinad Mutton Curry', 'category': 'curries', 'price': 420.00, 'diet': 'nonveg', 'prep_time': '15m'},
        {'id': 110, 'name': 'Butter Garlic Naan', 'category': 'breads', 'price': 65.00, 'diet': 'veg', 'prep_time': '5m'},
        {'id': 111, 'name': 'Tandoori Roti (Butter)', 'category': 'breads', 'price': 35.00, 'diet': 'veg', 'prep_time': '4m'},
        {'id': 112, 'name': 'Masala Dosa with Chutneys', 'category': 'south_indian', 'price': 120.00, 'diet': 'veg', 'prep_time': '6m'},
        {'id': 113, 'name': 'Ghee Podi Idli (4 pcs)', 'category': 'south_indian', 'price': 110.00, 'diet': 'veg', 'prep_time': '5m'},
        {'id': 114, 'name': 'Andhra Unlimited Meals', 'category': 'south_indian', 'price': 290.00, 'diet': 'veg', 'prep_time': '5m'},
        {'id': 115, 'name': 'Gulab Jamun with Rabdi', 'category': 'desserts', 'price': 140.00, 'diet': 'veg', 'prep_time': '3m'},
        {'id': 116, 'name': 'South Indian Filter Coffee', 'category': 'beverages', 'price': 55.00, 'diet': 'veg', 'prep_time': '4m'},
    ]

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'selected_table': request.GET.get('table', 'T-04 (AC Hall)')
    }
    return render(request, 'pos/terminal.html', context)
