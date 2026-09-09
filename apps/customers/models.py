from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from apps.core.models import BaseModel, Restaurant


class Customer(BaseModel):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('BLOCKED', 'Blocked'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=150, db_index=True)
    phone = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(blank=True)
    dob = models.DateField(null=True, blank=True)
    anniversary = models.DateField(null=True, blank=True)
    total_visits = models.PositiveIntegerField(default=0)
    total_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    loyalty_points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        db_table = 'df_customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'phone'], name='unique_customer_phone_per_restaurant'),
            CheckConstraint(condition=Q(total_spend__gte=0), name='customer_total_spend_non_negative'),
            CheckConstraint(condition=Q(loyalty_points__gte=0), name='customer_loyalty_points_non_negative'),
        ]
        indexes = [
            models.Index(fields=['restaurant', 'phone']),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone})"


class CustomerAddress(BaseModel):
    ADDRESS_TYPES = [
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='HOME')
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_customer_addresses'
        verbose_name = 'Customer Address'
        verbose_name_plural = 'Customer Addresses'

    def __str__(self):
        return f"{self.customer.name} - {self.address_type} ({self.city})"


class CustomerPreference(BaseModel):
    DIETARY_PREFERENCES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('JAIN', 'Jain Friendly'),
    ]

    SPICE_LEVELS = [
        ('LOW', 'Mild'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'Spicy'),
        ('EXTRA_HIGH', 'Extra Spicy'),
    ]

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='preference')
    dietary_preference = models.CharField(max_length=20, choices=DIETARY_PREFERENCES, default='NON_VEG')
    spice_tolerance = models.CharField(max_length=20, choices=SPICE_LEVELS, default='MEDIUM')
    allergies = models.CharField(max_length=255, blank=True)
    favorite_dishes = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)

    class Meta:
        db_table = 'df_customer_preferences'
        verbose_name = 'Customer Preference'
        verbose_name_plural = 'Customer Preferences'

    def __str__(self):
        return f"Preferences for {self.customer.name}"


class CustomerOrderHistory(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_history_records')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='customer_history')
    order_date = models.DateTimeField(db_index=True)
    order_amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_type = models.CharField(max_length=20)
    item_summary = models.TextField(blank=True)

    class Meta:
        db_table = 'df_customer_order_histories'
        verbose_name = 'Customer Order History'
        verbose_name_plural = 'Customer Order Histories'
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.customer.name} - Order on {self.order_date.strftime('%Y-%m-%d')} (₹{self.order_amount})"


class CustomerReservationHistory(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservation_history_records')
    reservation = models.ForeignKey('tables.Reservation', on_delete=models.CASCADE, related_name='customer_history')
    reservation_date = models.DateTimeField(db_index=True)
    party_size = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'df_customer_reservation_histories'
        verbose_name = 'Customer Reservation History'
        verbose_name_plural = 'Customer Reservation Histories'
        ordering = ['-reservation_date']

    def __str__(self):
        return f"{self.customer.name} - Res on {self.reservation_date.strftime('%Y-%m-%d')} ({self.party_size} guests)"
