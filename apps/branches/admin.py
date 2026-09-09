"""Branch Django Admin."""
from django.contrib import admin
from apps.branches.models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'phone', 'total_seating_capacity', 'is_active')
    list_filter = ('city', 'is_active')
    search_fields = ('name', 'code', 'city')
