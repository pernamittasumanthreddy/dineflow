"""Menu Django Admin Registration."""
from django.contrib import admin
from apps.menu.models import Category, MenuItem, MenuItemVariant, MenuItemAddon, RecipeItem

class MenuItemVariantInline(admin.TabularInline):
    model = MenuItemVariant
    extra = 1

class MenuItemAddonInline(admin.TabularInline):
    model = MenuItemAddon
    extra = 1

class RecipeItemInline(admin.TabularInline):
    model = RecipeItem
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('display_order', 'is_active')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'food_type', 'base_price', 'tax_rate_percent', 'is_available', 'is_featured')
    list_filter = ('category', 'food_type', 'is_available', 'is_featured')
    search_fields = ('name', 'code', 'description')
    list_editable = ('base_price', 'is_available', 'is_featured')
    inlines = [MenuItemVariantInline, MenuItemAddonInline, RecipeItemInline]
