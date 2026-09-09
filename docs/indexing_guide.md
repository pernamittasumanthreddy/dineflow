# DineFlow Database Indexing and Performance Optimization Guide

## 1. Indexing Strategy

Indexes in DineFlow are designed strictly around active query patterns rather than blindly indexing every column. Every index has a clear operational justification:

### 1.1 Multi-Tenant Isolation Indexes
- `df_branches(restaurant_id, is_active)`: High-velocity lookup of active restaurant locations.
- `df_orders(branch_id, status, placed_at)`: The core index for Kitchen Display System (KDS) and POS active order queues.
- `df_orders(branch_id, order_type, placed_at)`: Powers channel-specific filtering (Dine-in vs Swiggy/Zomato deliveries).
- `df_stocks(branch_id, inventory_item_id)`: Instant O(1) stock checks during order placement and recipe BOM consumption.

### 1.2 CRM & Identity Lookup Indexes
- `df_users(email, is_active)` and `df_users(phone, is_active)`: Fast JWT authentication and staff lookup.
- `df_customers(restaurant_id, phone)`: POS telephone lookup when diner arrives or calls for takeaway.
- `df_reservations(branch_id, reservation_time, status)`: Table booking calendar and slot availability checks.

### 1.3 Financial & Audit Temporal Indexes
- `df_invoices(branch_id, invoice_date)`: Monthly GST GSTR-1 and GSTR-3B report generation.
- `df_payments(branch_id, paid_at, status)`: Day-end drawer cash/UPI tender reconciliation.
- `df_audit_logs(model_name, object_id)`: Quick inspection of the audit trail for any single entity.
- `df_audit_logs(action, timestamp)`: Security and compliance event scanning.

---

## 2. Django ORM Query Performance Optimization

### 2.1 Eliminating N+1 Query Antipatterns

#### Bad Pattern (Triggers N database queries):
```python
orders = Order.objects.filter(branch=branch, status='PLACED')
for order in orders:
    print(order.table.table_number)      # 1 query per order
    print(order.customer.name)          # 1 query per order
    for item in order.items.all():      # 1 query per order
        print(item.menu_item.name)      # 1 query per item
```

#### Optimized Pattern (Executes in exactly 2 queries via joins and batch prefetching):
```python
orders = Order.objects.filter(branch=branch, status='PLACED')\
    .select_related('table', 'customer')\
    .prefetch_related(
        'items__menu_item',
        'items__menu_variant',
        'items__addons__addon'
    )
```

### 2.2 Dashboard Aggregation Queries
Rather than loading instances into Python memory for calculation, use database-native aggregations:

```python
from django.db.models import Sum, Count, Avg, F

daily_summary = Order.objects.filter(
    branch=branch,
    placed_at__date=today
).aggregate(
    total_sales=Sum('final_amount'),
    total_orders=Count('id'),
    avg_ticket=Avg('final_amount'),
    total_tax=Sum('tax_amount')
)
```
