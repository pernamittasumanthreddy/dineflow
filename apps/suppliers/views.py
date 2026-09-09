from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['inventory', 'manager', 'owner', 'super_admin'])
def supplier_list(request):
    """
    Vendor & Supplier Master Directory.
    """
    suppliers = [
        {'code': 'SUP-101', 'name': 'Sri Balaji Agro Ltd', 'category': 'Grains & Rice', 'contact_person': 'Ramesh Balaji', 'phone': '+91 98480 99887', 'city': 'Guntur / Hyderabad', 'gstin': '36AAACB1234F1Z1', 'payment_terms': 'Net 15 Days', 'rating': '4.9 ★', 'status': 'active'},
        {'code': 'SUP-102', 'name': 'Heritage Dairy Foods', 'category': 'Milk, Paneer, Curd', 'contact_person': 'Suresh Kumar', 'phone': '+91 98490 88776', 'city': 'Bangalore', 'gstin': '29AABCH5678J1Z2', 'payment_terms': 'Weekly Cycle', 'rating': '4.8 ★', 'status': 'active'},
        {'code': 'SUP-103', 'name': 'Suguna Poultry Farm', 'category': 'Fresh Chicken & Eggs', 'contact_person': 'M. Sundaram', 'phone': '+91 94433 22110', 'city': 'Coimbatore / Chennai', 'gstin': '33AABCS9012K1Z3', 'payment_terms': 'Daily COD', 'rating': '5.0 ★', 'status': 'active'},
        {'code': 'SUP-104', 'name': 'MDH Spices & Masala Hub', 'category': 'Pure Spices & Oils', 'contact_person': 'Vipin Gulati', 'phone': '+91 98110 33445', 'city': 'Delhi NCR', 'gstin': '07AAACM3456L1Z4', 'payment_terms': 'Net 30 Days', 'rating': '4.7 ★', 'status': 'active'},
        {'code': 'SUP-105', 'name': 'Amul India (GCMMF)', 'category': 'Butter, Ghee, Cream', 'contact_person': 'K. Patel', 'phone': '+91 98250 11223', 'city': 'Anand / Mumbai', 'gstin': '24AAACG1234D1Z5', 'payment_terms': 'Net 15 Days', 'rating': '5.0 ★', 'status': 'active'},
    ]
    context = {
        'page_title': 'Suppliers & Vendor Registry',
        'suppliers': suppliers
    }
    return render(request, 'suppliers/list.html', context)
