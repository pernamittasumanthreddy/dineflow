from django.shortcuts import render

def item_list(request):
    """
    Menu Master Catalog (Dishes, Dietary tags, Prices, Taxes).
    """
    items = [
        {'id': 101, 'name': 'Hyderabadi Chicken Dum Biryani', 'category': 'Biryani & Rice', 'price': 340.00, 'cost': 118.50, 'margin': '65.1%', 'diet': 'nonveg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 102, 'name': 'Special Mutton Handi Biryani', 'category': 'Biryani & Rice', 'price': 460.00, 'cost': 168.00, 'margin': '63.5%', 'diet': 'nonveg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 103, 'name': 'Royal Veg Dum Biryani', 'category': 'Biryani & Rice', 'price': 240.00, 'cost': 62.00, 'margin': '74.2%', 'diet': 'veg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 104, 'name': 'Andhra Spicy Chicken 65', 'category': 'Tandoor & Starters', 'price': 280.00, 'cost': 94.00, 'margin': '66.4%', 'diet': 'nonveg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 105, 'name': 'Murg Malai Tikka (8 pcs)', 'category': 'Tandoor & Starters', 'price': 340.00, 'cost': 122.00, 'margin': '64.1%', 'diet': 'nonveg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 106, 'name': 'Paneer Tikka Shashlik', 'category': 'Tandoor & Starters', 'price': 290.00, 'cost': 88.00, 'margin': '69.7%', 'diet': 'veg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 107, 'name': 'Paneer Butter Masala', 'category': 'Main Curries', 'price': 260.00, 'cost': 76.00, 'margin': '70.8%', 'diet': 'veg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 108, 'name': 'Dal Makhani Handi', 'category': 'Main Curries', 'price': 220.00, 'cost': 48.00, 'margin': '78.2%', 'diet': 'veg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 109, 'name': 'Chettinad Mutton Curry', 'category': 'Main Curries', 'price': 420.00, 'cost': 152.00, 'margin': '63.8%', 'diet': 'nonveg', 'tax_rate': '5% GST', 'status': 'active'},
        {'id': 110, 'name': 'Butter Garlic Naan', 'category': 'Indian Breads', 'price': 65.00, 'cost': 11.50, 'margin': '82.3%', 'diet': 'veg', 'tax_rate': '5% GST', 'status': 'active'},
    ]
    context = {
        'page_title': 'Menu Master Items',
        'items': items
    }
    return render(request, 'menu/item_list.html', context)

def categories(request):
    """
    Category & Modifier Add-on Management.
    """
    categories_list = [
        {'name': 'Biryani & Rice', 'code': 'CAT-BIR', 'items_count': 14, 'station': 'Biryani Station', 'tax_slab': '5% GST (SAC 996331)'},
        {'name': 'Tandoor & Starters', 'code': 'CAT-TAN', 'items_count': 22, 'station': 'Tandoor Station', 'tax_slab': '5% GST (SAC 996331)'},
        {'name': 'Main Curries & Gravies', 'code': 'CAT-CUR', 'items_count': 28, 'station': 'Curry Station', 'tax_slab': '5% GST (SAC 996331)'},
        {'name': 'Indian Breads (Roti/Naan)', 'code': 'CAT-BRD', 'items_count': 12, 'station': 'Tandoor Station', 'tax_slab': '5% GST (SAC 996331)'},
        {'name': 'South Indian Tiffins', 'code': 'CAT-STF', 'items_count': 16, 'station': 'Tiffin Station', 'tax_slab': '5% GST (SAC 996331)'},
        {'name': 'Desserts & Sweets', 'code': 'CAT-DES', 'items_count': 10, 'station': 'Bakery Station', 'tax_slab': '5% GST (SAC 996331)'},
        {'name': 'Beverages & Mocktails', 'code': 'CAT-BEV', 'items_count': 18, 'station': 'Bar & Beverage', 'tax_slab': '18% GST (SAC 996332)'},
    ]
    context = {
        'page_title': 'Menu Categories & Modifiers',
        'categories': categories_list
    }
    return render(request, 'menu/categories.html', context)

def recipe_costing(request):
    """
    Recipe Costing, Ingredient Depletion & Margin Engineering.
    """
    recipes = [
        {
            'dish': 'Hyderabadi Chicken Dum Biryani',
            'selling_price': 340.00,
            'cogs': 118.50,
            'profit': 221.50,
            'margin_pct': 65.1,
            'diet': 'nonveg',
            'ingredients': [
                {'name': 'Tender Curry Cut Chicken', 'qty': '250g', 'cost': '₹55.00'},
                {'name': 'India Gate Classic Basmati Rice', 'qty': '180g', 'cost': '₹23.50'},
                {'name': 'Pure Desi Cow Ghee', 'qty': '35g', 'cost': '₹19.20'},
                {'name': 'Fresh Curd (Dahi)', 'qty': '80g', 'cost': '₹4.80'},
                {'name': 'Biryani Masala & Saffron Milk', 'qty': '15g', 'cost': '₹16.00'},
            ]
        },
        {
            'dish': 'Paneer Butter Masala',
            'selling_price': 260.00,
            'cogs': 76.00,
            'profit': 184.00,
            'margin_pct': 70.8,
            'diet': 'veg',
            'ingredients': [
                {'name': 'Fresh Malai Paneer Cubes', 'qty': '200g', 'cost': '₹46.00'},
                {'name': 'Amul Fresh Cooking Cream', 'qty': '40ml', 'cost': '₹12.00'},
                {'name': 'Rich Tomato & Cashew Gravy Base', 'qty': '150g', 'cost': '₹14.00'},
                {'name': 'Kasuri Methi & Butter', 'qty': '10g', 'cost': '₹4.00'},
            ]
        }
    ]
    context = {
        'page_title': 'Recipe Costing & Menu Engineering',
        'recipes': recipes
    }
    return render(request, 'menu/recipe_costing.html', context)
