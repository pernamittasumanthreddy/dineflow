from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant, User


class Order(BaseModel):
    ORDER_TYPES = [
        ('DINE_IN', 'Dine-in'),
        ('TAKEAWAY', 'Takeaway'),
        ('DELIVERY', 'Delivery'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PLACED', 'Placed'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('SERVED', 'Served'),
        ('BILLED', 'Billed'),
        ('PAID', 'Paid'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, default='DINE_IN', db_index=True)
    table = models.ForeignKey(
        'tables.RestaurantTable', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    waiter = models.ForeignKey(
        'employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_served'
    )
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED', db_index=True)

    total_item_count = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    packaging_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    service_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    round_off = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    placed_at = models.DateTimeField(default=timezone.now, db_index=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'df_orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        constraints = [
            CheckConstraint(condition=Q(subtotal__gte=0), name='order_subtotal_non_negative'),
            CheckConstraint(condition=Q(discount_amount__gte=0), name='order_discount_non_negative'),
            CheckConstraint(condition=Q(tax_amount__gte=0), name='order_tax_non_negative'),
            CheckConstraint(condition=Q(final_amount__gte=0), name='order_final_amount_non_negative'),
        ]
        indexes = [
            models.Index(fields=['branch', 'status', 'placed_at']),
            models.Index(fields=['branch', 'order_type', 'placed_at']),
        ]

    def __str__(self):
        return f"Order #{self.order_number} ({self.order_type}) - ₹{self.final_amount} [{self.status}]"


class OrderItem(BaseModel):
    ITEM_STATUS_CHOICES = [
        ('RECEIVED', 'Received'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('SERVED', 'Served'),
        ('CANCELLED', 'Cancelled'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.PROTECT, related_name='order_items')
    menu_variant = models.ForeignKey(
        'menu.MenuVariant', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default='RECEIVED')

    class Meta:
        db_table = 'df_order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        constraints = [
            CheckConstraint(condition=Q(quantity__gt=0), name='order_item_quantity_positive'),
            CheckConstraint(condition=Q(unit_price__gte=0), name='order_item_unit_price_non_negative'),
            CheckConstraint(condition=Q(total_price__gte=0), name='order_item_total_price_non_negative'),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.order_number})"


class OrderItemAddon(BaseModel):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='addons')
    addon = models.ForeignKey('menu.MenuAddon', on_delete=models.PROTECT, related_name='order_item_addons')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'df_order_item_addons'
        verbose_name = 'Order Item Addon'
        verbose_name_plural = 'Order Item Addons'
        constraints = [
            CheckConstraint(condition=Q(quantity__gt=0), name='order_addon_quantity_positive'),
            CheckConstraint(condition=Q(unit_price__gte=0), name='order_addon_unit_price_non_negative'),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.addon.name} for {self.order_item.menu_item.name}"


class OrderStatusHistory(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_status_changes'
    )
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_order_status_history'
        verbose_name = 'Order Status History'
        verbose_name_plural = 'Order Status Histories'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Order #{self.order.order_number}: {self.old_status} -> {self.new_status}"


class OrderDiscount(BaseModel):
    DISCOUNT_TYPES = [
        ('PERCENTAGE', 'Percentage'),
        ('FLAT', 'Flat Amount'),
        ('COUPON', 'Coupon Code'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discounts')
    coupon = models.ForeignKey(
        'offers.Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_discounts'
    )
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='FLAT')
    rate_or_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255, blank=True)
    applied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_order_discounts'
        verbose_name = 'Order Discount'
        verbose_name_plural = 'Order Discounts'
        constraints = [
            CheckConstraint(condition=Q(discount_amount__gte=0), name='order_discount_amt_non_negative')
        ]

    def __str__(self):
        return f"Discount ₹{self.discount_amount} on Order #{self.order.order_number}"


class OrderTax(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='taxes')
    tax_name = models.CharField(max_length=50)  # e.g., 'CGST', 'SGST', 'IGST'
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'df_order_taxes'
        verbose_name = 'Order Tax'
        verbose_name_plural = 'Order Taxes'
        constraints = [
            CheckConstraint(condition=Q(tax_amount__gte=0), name='order_tax_amount_non_negative'),
            CheckConstraint(condition=Q(rate__gte=0) & Q(rate__lte=100), name='order_tax_rate_valid_percent')
        ]

    def __str__(self):
        return f"{self.tax_name} ({self.rate}%): ₹{self.tax_amount}"


class OrderNote(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    is_customer_visible = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_order_notes'
        verbose_name = 'Order Note'
        verbose_name_plural = 'Order Notes'

    def __str__(self):
        return f"Note for Order #{self.order.order_number}"
