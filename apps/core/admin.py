from django.contrib import admin

from .models import (
    Branch,
    BranchSettings,
    Permission,
    Restaurant,
    RestaurantSettings,
    Role,
    User,
    UserRole,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'phone', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active', 'is_deleted']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_system_role']
    search_fields = ['name', 'code']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'module']
    search_fields = ['name', 'codename', 'module']
    list_filter = ['module']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'restaurant', 'branch', 'is_active']
    list_filter = ['role', 'restaurant', 'branch', 'is_active']


class RestaurantSettingsInline(admin.StackedInline):
    model = RestaurantSettings
    can_delete = False


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'gstin', 'fssai_license', 'phone', 'email', 'is_active']
    search_fields = ['name', 'code', 'gstin', 'phone']
    list_filter = ['is_active']
    inlines = [RestaurantSettingsInline]


class BranchSettingsInline(admin.StackedInline):
    model = BranchSettings
    can_delete = False


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'code', 'city', 'state', 'phone', 'is_active']
    search_fields = ['name', 'code', 'city', 'state']
    list_filter = ['restaurant', 'city', 'state', 'is_active']
    inlines = [BranchSettingsInline]
