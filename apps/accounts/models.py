"""DineFlow Accounts & Role-Based Authentication Models."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class RoleChoices(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    RESTAURANT_OWNER = 'RESTAURANT_OWNER', 'Restaurant Owner'
    MANAGER = 'MANAGER', 'Manager'
    KITCHEN_STAFF = 'KITCHEN_STAFF', 'Kitchen Staff'
    WAITER = 'WAITER', 'Waiter'
    CASHIER = 'CASHIER', 'Cashier'
    INVENTORY_MANAGER = 'INVENTORY_MANAGER', 'Inventory Manager'
    HR = 'HR', 'HR Manager'
    CUSTOMER = 'CUSTOMER', 'Customer'
    ANALYTICS_USER = 'ANALYTICS_USER', 'Analytics User'

class UserManager(BaseUserManager):
    """Custom user manager supporting email/phone registration."""
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        if not username:
            username = email.split('@')[0]
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', RoleChoices.SUPER_ADMIN)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    """Custom enterprise User model with RBAC and branch multi-tenancy."""
    email = models.EmailField('Email Address', unique=True, db_index=True)
    phone_number = models.CharField('Phone Number', max_length=15, blank=True, null=True, db_index=True)
    role = models.CharField('Role', max_length=30, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER, db_index=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Tenancy linkage
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    
    # Security tracking
    failed_login_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def display_name(self):
        return self.get_full_name() or self.username or self.email

    @property
    def is_super_admin(self):
        return self.role == RoleChoices.SUPER_ADMIN or self.is_superuser

    @property
    def is_restaurant_owner(self):
        return self.role == RoleChoices.RESTAURANT_OWNER or self.is_super_admin

    @property
    def is_manager(self):
        return self.role in [RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER, RoleChoices.SUPER_ADMIN]

    @property
    def is_kitchen_staff(self):
        return self.role in [RoleChoices.KITCHEN_STAFF, RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN]

    @property
    def is_cashier(self):
        return self.role in [RoleChoices.CASHIER, RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN]

    @property
    def is_waiter(self):
        return self.role in [RoleChoices.WAITER, RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN]

    @property
    def is_inventory_manager(self):
        return self.role in [RoleChoices.INVENTORY_MANAGER, RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN]

    @property
    def is_hr_manager(self):
        return self.role in [RoleChoices.HR, RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN]

    @property
    def is_analytics_user(self):
        return self.role in [RoleChoices.ANALYTICS_USER, RoleChoices.RESTAURANT_OWNER, RoleChoices.SUPER_ADMIN]

    def has_module_permission(self, module_name):
        """Granular server-side permission validation."""
        if self.is_super_admin:
            return True
        
        module_matrix = {
            'orders': [RoleChoices.MANAGER, RoleChoices.WAITER, RoleChoices.CASHIER, RoleChoices.RESTAURANT_OWNER],
            'kitchen': [RoleChoices.KITCHEN_STAFF, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'billing': [RoleChoices.CASHIER, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'payments': [RoleChoices.CASHIER, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'refunds': [RoleChoices.CASHIER, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'inventory': [RoleChoices.INVENTORY_MANAGER, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'purchases': [RoleChoices.INVENTORY_MANAGER, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'suppliers': [RoleChoices.INVENTORY_MANAGER, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'hr': [RoleChoices.HR, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'payroll': [RoleChoices.HR, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'attendance': [RoleChoices.HR, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER, RoleChoices.WAITER, RoleChoices.KITCHEN_STAFF, RoleChoices.CASHIER],
            'menu': [RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER],
            'tables': [RoleChoices.MANAGER, RoleChoices.WAITER, RoleChoices.CASHIER, RoleChoices.RESTAURANT_OWNER],
            'reservations': [RoleChoices.MANAGER, RoleChoices.WAITER, RoleChoices.CASHIER, RoleChoices.RESTAURANT_OWNER],
            'analytics': [RoleChoices.ANALYTICS_USER, RoleChoices.RESTAURANT_OWNER, RoleChoices.MANAGER],
            'reports': [RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER, RoleChoices.HR, RoleChoices.ANALYTICS_USER],
            'audit': [RoleChoices.RESTAURANT_OWNER, RoleChoices.SUPER_ADMIN],
            'settings': [RoleChoices.RESTAURANT_OWNER, RoleChoices.SUPER_ADMIN],
        }
        allowed_roles = module_matrix.get(module_name.lower(), [])
        return self.role in allowed_roles

class LoginHistory(models.Model):
    """Audit records of user login attempts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories', null=True, blank=True)
    attempted_email = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('LOCKED', 'Account Locked')]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.attempted_email} - {self.status} at {self.timestamp}"
