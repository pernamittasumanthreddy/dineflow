from django.contrib import admin
from .models import (
    Menu, MenuCategory, MenuItem, MenuVariant, MenuAddon,
    MenuItemAddon, PriceHistory, Recipe, FoodIngredient
)


class MenuVariantInline(admin.TabularInline):
    model = MenuVariant
    extra = 1


class MenuItemAddonInline(admin.TabularInline):
    model = MenuItemAddon
    extra = 1


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'dietary_type', 'is_available', 'is_recommended']
    list_filter = ['category__menu__restaurant', 'dietary_type', 'is_available', 'category']
    search_fields = ['name', 'short_code']
    inlines = [MenuVariantInline, MenuItemAddonInline]


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu', 'code', 'sort_order', 'is_active']
    list_filter = ['menu__restaurant', 'is_active']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'branch', 'menu_type', 'is_active']
    list_filter = ['restaurant', 'menu_type', 'is_active']


@admin.register(MenuAddon)
class MenuAddonAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'price', 'is_available']
    list_filter = ['restaurant', 'is_available']


class FoodIngredientInline(admin.TabularInline):
    model = FoodIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu_item', 'yield_servings', 'prep_time_minutes', 'cook_time_minutes']
    search_fields = ['title', 'menu_item__name']
    inlines = [FoodIngredientInline]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'menu_variant', 'old_price', 'new_price', 'effective_from', 'changed_by']
    list_filter = ['effective_from']
