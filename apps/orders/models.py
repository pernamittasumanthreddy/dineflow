"""Enterprise Order State Machine and POS Line Item Models."""
import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel, SoftDeleteModel

class OrderType(models.TextChoices):
    DINE_IN = 'DINE_IN', 'Dine-In'
    TAKEAWAY = 'TAKEAWAY', 'Takeaway / Counter'
    DELIVERY = 'DELIVERY', 'Home Delivery'

class OrderStatus(models.TextChoices):
    NEW = 'NEW', 'New'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    PREPARING = 'PREPARING', 'In Kitchen / Preparing'
    READY = 'READY', 'Ready for Serving / Pickup'
    COMPLETED = 'COMPLETED', 'Completed & Paid'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Order(TimeStampedModel, SoftDeleteModel):
    """Core transaction order entity traversing the POS & Kitchen lifecycle."""
    order_number = models.CharField('Order #', max_length=50, unique=True, db_index=True)
    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.DINE_IN)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        db_index=True
    )
    
    # Outlet & Entities
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    table = models.ForeignKey(
        'tables.RestaurantTable',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    server = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='served_orders',
        help_text='Waiter or cashier taking the order'
    )
    
    # Financials
    subtotal = models.DecimalField('Subtotal (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField('Discount (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField('GST Tax (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField('Grand Total (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_paid = models.BooleanField('Payment Settled', default=False, db_index=True)
    
    # Operations
    guest_count = models.PositiveIntegerField('Guest Count', default=1)
    special_instructions = models.TextField('Kitchen / Chef Notes', blank=True)
    cancellation_reason = models.TextField('Cancellation Reason', blank=True)
    
    # Timestamps
    confirmed_at = models.DateTimeField(null=True, blank=True)
    prep_started_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Restaurant Order'
        verbose_name_plural = 'Restaurant Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} [{self.get_order_type_display()}] - ₹{self.grand_total} ({self.status})"

    def recalculate_totals(self):
        """Recalculate order subtotal, GST, and grand total from active line items."""
        total_subtotal = Decimal('0.00')
        total_tax = Decimal('0.00')
        
        for item in self.items.all():
            total_subtotal += item.item_total
            tax_rate = (item.menu_item.tax_rate_percent or Decimal('5.00')) / Decimal('100.00')
            total_tax += (item.item_total * tax_rate)
            
        self.subtotal = total_subtotal
        self.tax_amount = total_tax.quantize(Decimal('0.01'))
        self.grand_total = (self.subtotal - self.discount_amount + self.tax_amount).quantize(Decimal('0.01'))
        self.save(update_fields=['subtotal', 'tax_amount', 'grand_total'])

class OrderItem(TimeStampedModel):
    """Line item dish with specific variant, quantity, and cooking notes."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey(
        'menu.MenuItemVariant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total = models.DecimalField(max_digits=12, decimal_places=2)
    kitchen_notes = models.CharField(max_length=255, blank=True, help_text='e.g., Less spicy, no onions, extra crispy')
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('COOKING', 'Cooking'), ('READY', 'Ready'), ('SERVED', 'Served')],
        default='PENDING'
    )

    class Meta:
        verbose_name = 'Order Line Item'
        verbose_name_plural = 'Order Line Items'

    def __str__(self):
        variant_str = f" ({self.variant.name})" if self.variant else ""
        return f"{self.quantity}x {self.menu_item.name}{variant_str} - ₹{self.item_total}"

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.variant.price if self.variant else self.menu_item.base_price
        self.item_total = (Decimal(str(self.unit_price)) * Decimal(str(self.quantity))).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
