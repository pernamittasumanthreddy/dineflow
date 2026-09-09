import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class BaseModel(models.Model):
    """
    Abstract base model providing UUID primary key, auditing timestamps,
    and soft deletion functionality across the entire DineFlow architecture.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        if not phone:
            raise ValueError('Phone number is required')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Core User model supporting role-based access control, multi-branch operations,
    and auditability.
    """
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = CustomUserManager()
    all_objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name']

    class Meta:
        db_table = 'df_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['phone', 'is_active']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.email

    def get_short_name(self):
        return self.first_name or self.email


class Permission(BaseModel):
    """
    Fine-grained system permissions for restaurant ERP operations.
    """
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)
    module = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'df_permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        ordering = ['module', 'codename']

    def __str__(self):
        return f"{self.module} | {self.name}"


class Role(BaseModel):
    """
    Predefined or customized operational roles within DineFlow.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_system_role = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    class Meta:
        db_table = 'df_roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class Restaurant(BaseModel):
    """
    Multi-tenant Root Organization model representing a restaurant enterprise.
    """
    name = models.CharField(max_length=200, db_index=True)
    legal_name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    gstin = models.CharField(max_length=15, blank=True, help_text="Indian GST Identification Number")
    fssai_license = models.CharField(max_length=20, blank=True, help_text="Food Safety Standard Authority of India License")
    pan_number = models.CharField(max_length=10, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='restaurants/logos/', null=True, blank=True)
    currency = models.CharField(max_length=10, default='INR')
    currency_symbol = models.CharField(max_length=5, default='₹')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_restaurants'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return f"{self.name} ({self.code})"


class RestaurantSettings(BaseModel):
    """
    Tenant-level configuration parameters for business rules and invoicing.
    """
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='settings')
    fiscal_year_start_month = models.PositiveSmallIntegerField(default=4, help_text="1=Jan, 4=Apr (standard Indian fiscal year)")
    default_service_charge_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    invoice_prefix = models.CharField(max_length=10, default='INV')
    kot_prefix = models.CharField(max_length=10, default='KOT')
    po_prefix = models.CharField(max_length=10, default='PO')
    grn_prefix = models.CharField(max_length=10, default='GRN')
    auto_generate_kot = models.BooleanField(default=True)
    round_off_bills = models.BooleanField(default=True)
    loyalty_points_per_rupee = models.DecimalField(max_digits=6, decimal_places=4, default=0.05)
    loyalty_point_redemption_value = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)

    class Meta:
        db_table = 'df_restaurant_settings'
        verbose_name = 'Restaurant Settings'
        verbose_name_plural = 'Restaurant Settings'

    def __str__(self):
        return f"Settings for {self.restaurant.name}"


class Branch(BaseModel):
    """
    Branch location belonging to a Restaurant entity.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, db_index=True)
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_headquarters = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'code'], name='unique_branch_code_per_restaurant')
        ]
        indexes = [
            models.Index(fields=['restaurant', 'city']),
            models.Index(fields=['restaurant', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.city} ({self.restaurant.name})"


class BranchSettings(BaseModel):
    """
    Branch-specific operational toggles and thresholds.
    """
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='settings')
    dine_in_enabled = models.BooleanField(default=True)
    takeaway_enabled = models.BooleanField(default=True)
    delivery_enabled = models.BooleanField(default=True)
    table_reservation_enabled = models.BooleanField(default=True)
    auto_confirm_orders = models.BooleanField(default=False)
    delivery_radius_km = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    minimum_order_delivery = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    opening_time = models.TimeField(default='10:00:00')
    closing_time = models.TimeField(default='23:00:00')

    class Meta:
        db_table = 'df_branch_settings'
        verbose_name = 'Branch Settings'
        verbose_name_plural = 'Branch Settings'

    def __str__(self):
        return f"Settings for {self.branch.name}"


class UserRole(BaseModel):
    """
    Scoped user-to-role assignment, enabling multi-tenant authority.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name='user_roles')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='user_roles')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_user_roles'
        verbose_name = 'User Role Assignment'
        verbose_name_plural = 'User Role Assignments'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role', 'restaurant', 'branch'],
                name='unique_user_role_assignment'
            )
        ]

    def __str__(self):
        scope = f" | {self.restaurant.name}" if self.restaurant else " | System Wide"
        if self.branch:
            scope += f" - {self.branch.name}"
        return f"{self.user.email} -> {self.role.name}{scope}"
