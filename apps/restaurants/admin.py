"""Restaurant Django Admin."""
from django.contrib import admin
from apps.restaurants.models import Restaurant, RestaurantSetting

class RestaurantSettingInline(admin.StackedInline):
    model = RestaurantSetting
    can_delete = False

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'gstin', 'fssai_number', 'city', 'phone', 'is_active')
    search_fields = ('name', 'gstin', 'fssai_number', 'city')
    inlines = [RestaurantSettingInline]

@admin.register(RestaurantSetting)
class RestaurantSettingAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'default_cgst_percent', 'default_sgst_percent', 'is_tax_inclusive')
