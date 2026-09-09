"""Tables Django Admin."""
from django.contrib import admin
from apps.tables.models import FloorSection, RestaurantTable

@admin.register(FloorSection)
class FloorSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'floor_number', 'is_active')
    list_filter = ('branch', 'floor_number')

@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'branch', 'section', 'seating_capacity', 'status', 'is_active')
    list_filter = ('branch', 'section', 'status')
    list_editable = ('status',)
    search_fields = ('table_number',)
