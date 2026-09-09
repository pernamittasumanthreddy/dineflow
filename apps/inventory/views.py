from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['inventory', 'manager', 'owner', 'super_admin'])
def stock_ledger(request):
    """
    Raw Material Stock Inventory Ledger (Kg, Litres, Bags, Packets).
    """
    stock_items = [
        {'code': 'ING-1001', 'name': 'India Gate Classic Basmati Rice', 'category': 'Grains & Rice', 'on_hand': 12.5, 'unit': 'kg', 'buffer_min': 30.0, 'unit_cost': 130.00, 'total_value': 1625.00, 'status': 'low_stock', 'supplier': 'Sri Balaji Agro Ltd'},
        {'code': 'ING-1002', 'name': 'Fresh Malai Paneer Block', 'category': 'Dairy Products', 'on_hand': 4.2, 'unit': 'kg', 'buffer_min': 15.0, 'unit_cost': 230.00, 'total_value': 966.00, 'status': 'low_stock', 'supplier': 'Heritage Dairy'},
        {'code': 'ING-1003', 'name': 'Pure Desi Cow Ghee (Tin)', 'category': 'Oils & Fats', 'on_hand': 3.0, 'unit': 'L', 'buffer_min': 10.0, 'unit_cost': 580.00, 'total_value': 1740.00, 'status': 'low_stock', 'supplier': 'Amul India'},
        {'code': 'ING-1004', 'name': 'Tender Curry Cut Fresh Chicken', 'category': 'Poultry & Meat', 'on_hand': 45.0, 'unit': 'kg', 'buffer_min': 20.0, 'unit_cost': 220.00, 'total_value': 9900.00, 'status': 'in_stock', 'supplier': 'Suguna Poultry'},
        {'code': 'ING-1005', 'name': 'Kashmiri Red Chili Powder', 'category': 'Spices & Condiments', 'on_hand': 1.8, 'unit': 'kg', 'buffer_min': 5.0, 'unit_cost': 380.00, 'total_value': 684.00, 'status': 'low_stock', 'supplier': 'MDH Spices Hub'},
        {'code': 'ING-1006', 'name': 'Amul Fresh Cooking Cream (1L)', 'category': 'Dairy Products', 'on_hand': 18.0, 'unit': 'Packets', 'buffer_min': 10.0, 'unit_cost': 210.00, 'total_value': 3780.00, 'status': 'in_stock', 'supplier': 'Amul India'},
    ]
    context = {
        'page_title': 'Raw Materials Stock Ledger',
        'stock_items': stock_items
    }
    return render(request, 'inventory/stock_ledger.html', context)

@role_required(['inventory', 'manager', 'owner', 'super_admin'])
def purchase_orders(request):
    """
    Purchase Orders (PO), Inwarding & Goods Receipt Notes (GRN).
    """
    po_list = [
        {'po_num': 'PO-2026-0841', 'supplier': 'Sri Balaji Agro Ltd', 'date': '08/09/2026', 'items_count': 'Basmati Rice (100kg), Sona Masoori (50kg)', 'amount': 18500.00, 'grn_status': 'Inwarded / GRN-902', 'status': 'approved'},
        {'po_num': 'PO-2026-0842', 'supplier': 'Heritage Dairy', 'date': '09/09/2026', 'items_count': 'Paneer (30kg), Fresh Curd (50kg)', 'amount': 9400.00, 'grn_status': 'Awaiting Delivery', 'status': 'pending'},
        {'po_num': 'PO-2026-0843', 'supplier': 'MDH Spices Hub', 'date': '09/09/2026', 'items_count': 'Chili Powder (10kg), Garam Masala (5kg)', 'amount': 6200.00, 'grn_status': 'Awaiting Delivery', 'status': 'pending'},
    ]
    context = {
        'page_title': 'Purchase Orders & GRN Management',
        'po_list': po_list
    }
    return render(request, 'inventory/purchase_orders.html', context)

@role_required(['inventory', 'kitchen', 'manager', 'owner', 'super_admin'])
def waste_log(request):
    """
    Kitchen Spoilage & Ingredient Waste Tracker.
    """
    waste_records = [
        {'id': 'WST-401', 'date': 'Today, 11:30 AM', 'item': 'Fresh Tomatoes (Overripe)', 'qty': '4.5 kg', 'cost': 180.00, 'reason': 'Over-ripened during transport', 'chef': 'Chef Sanjeev'},
        {'id': 'WST-402', 'date': 'Yesterday', 'item': 'Biryani Rice Surplus Batch', 'qty': '3.2 kg', 'cost': 320.00, 'reason': 'Unsold afternoon buffet excess', 'chef': 'Chef Naresh'},
    ]
    context = {
        'page_title': 'Kitchen Spoilage & Waste Log',
        'waste_records': waste_records
    }
    return render(request, 'inventory/waste_log.html', context)
