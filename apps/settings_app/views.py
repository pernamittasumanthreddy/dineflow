from django.shortcuts import render
from apps.accounts.decorators import role_required

@role_required(['super_admin', 'owner'])
def branches(request):
    """
    Multi-Branch Outlet Management.
    """
    branch_records = [
        {'id': 1, 'name': 'Indiranagar Main (Bangalore)', 'code': 'BLR-IND-01', 'city': 'Bangalore', 'gstin': '29AABCS1429B1Z5', 'fssai': '11223334000121', 'tables': 28, 'staff_count': 22, 'status': 'active'},
        {'id': 2, 'name': 'Banjara Hills Flagship (Hyderabad)', 'code': 'HYD-BAN-01', 'city': 'Hyderabad', 'gstin': '36AABCS1429B1Z8', 'fssai': '13622014000889', 'tables': 36, 'staff_count': 26, 'status': 'active'},
        {'id': 3, 'name': 'Connaught Place (New Delhi)', 'code': 'DEL-CP-01', 'city': 'New Delhi', 'gstin': '07AABCS1429B1Z2', 'fssai': '10721008000456', 'tables': 24, 'staff_count': 18, 'status': 'active'},
        {'id': 4, 'name': 'Anna Nagar Central (Chennai)', 'code': 'CHN-ANN-01', 'city': 'Chennai', 'gstin': '33AABCS1429B1Z4', 'fssai': '13320015000782', 'tables': 30, 'staff_count': 20, 'status': 'active'},
        {'id': 5, 'name': 'Hitec City Cloud Kitchen (Hyderabad)', 'code': 'HYD-HIT-01', 'city': 'Hyderabad', 'gstin': '36AABCS1429B1Z8', 'fssai': '13623019000341', 'tables': 0, 'staff_count': 12, 'status': 'active'},
    ]
    context = {
        'page_title': 'Branch Management',
        'branch_records': branch_records
    }
    return render(request, 'settings/branches.html', context)

@role_required(['super_admin', 'owner'])
def roles_permissions(request):
    """
    Role-Based Access Control (RBAC) Permissions Matrix.
    """
    matrix = [
        {'module': 'Front of House Touch POS', 'owner': 'Full Access', 'manager': 'Full Access', 'kitchen': 'No Access', 'waiter': 'Punch Only', 'cashier': 'Full Access', 'hr': 'No Access'},
        {'module': 'Kitchen Display System (KDS)', 'owner': 'View Only', 'manager': 'Full Access', 'kitchen': 'Full Access', 'waiter': 'View Only', 'cashier': 'No Access', 'hr': 'No Access'},
        {'module': 'Bill Void & Discounts', 'owner': 'Full Access', 'manager': 'Authorized Pin', 'kitchen': 'No Access', 'waiter': 'No Access', 'cashier': 'Requires Pin', 'hr': 'No Access'},
        {'module': 'Raw Material Inventory & PO', 'owner': 'Full Access', 'manager': 'Full Access', 'kitchen': 'Deplete Only', 'waiter': 'No Access', 'cashier': 'No Access', 'hr': 'No Access'},
        {'module': 'Indian Payroll & Salary Slips', 'owner': 'Full Access', 'manager': 'No Access', 'kitchen': 'No Access', 'waiter': 'No Access', 'cashier': 'No Access', 'hr': 'Full Access'},
        {'module': 'Financial P&L & GSTR Exports', 'owner': 'Full Access', 'manager': 'Shift Only', 'kitchen': 'No Access', 'waiter': 'No Access', 'cashier': 'Z-Report Only', 'hr': 'No Access'},
    ]
    context = {
        'page_title': 'Roles & RBAC Permissions Matrix',
        'matrix': matrix
    }
    return render(request, 'settings/roles_permissions.html', context)

@role_required(['super_admin', 'owner'])
def audit_logs(request):
    """
    Immutable Security & Action Audit Trail.
    """
    logs = [
        {'id': 'AUD-9021', 'time': '09/09/2026, 14:32:10', 'user': 'Sneha Reddy (Cashier)', 'action': 'Settled Bill #INV-892401', 'module': 'Billing', 'ip': '192.168.1.104', 'status': 'success'},
        {'id': 'AUD-9020', 'time': '09/09/2026, 14:28:44', 'user': 'Ravi Teja (Captain)', 'action': 'Fired KOT #1042 to Kitchen', 'module': 'POS', 'ip': '192.168.1.112', 'status': 'success'},
        {'id': 'AUD-9019', 'time': '09/09/2026, 14:10:15', 'user': 'Pavan Varma (Owner)', 'action': 'Approved PO-2026-0842 (₹9,400)', 'module': 'Inventory', 'ip': '192.168.1.101', 'status': 'success'},
        {'id': 'AUD-9018', 'time': '09/09/2026, 13:45:00', 'user': 'System Cron Engine', 'action': 'Automated SQLite Snapshot Backup', 'module': 'System', 'ip': '127.0.0.1', 'status': 'success'},
    ]
    context = {
        'page_title': 'Audit Logs & Security Trail',
        'logs': logs
    }
    return render(request, 'settings/audit_logs.html', context)

@role_required(['super_admin'])
def backup_restore(request):
    """
    Database Backup & Disaster Recovery.
    """
    backups = [
        {'filename': 'dineflow_db_backup_20260909_1400.sqlite3', 'size': '24.8 MB', 'created_at': '09/09/2026, 14:00', 'type': 'Automated Hourly Snapshot', 'status': 'verified'},
        {'filename': 'dineflow_db_backup_20260909_0000.sqlite3', 'size': '24.2 MB', 'created_at': '09/09/2026, 00:00', 'type': 'Daily Midnight Cold Backup', 'status': 'verified'},
        {'filename': 'dineflow_db_backup_20260908_0000.sqlite3', 'size': '23.8 MB', 'created_at': '08/09/2026, 00:00', 'type': 'Daily Midnight Cold Backup', 'status': 'verified'},
    ]
    context = {
        'page_title': 'Database Backup & Restore',
        'backups': backups
    }
    return render(request, 'settings/backup_restore.html', context)

@role_required(['super_admin', 'owner'])
def general(request):
    """
    General System & Hardware Configuration.
    """
    context = {
        'page_title': 'ERP Settings & Hardware Configuration',
    }
    return render(request, 'settings/general.html', context)
