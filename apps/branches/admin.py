"""Branch Django Admin."""
from django.contrib import admin
from apps.branches.models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'manager', 'total_seating_capacity', 'is_active')
    search_fields = ('name', 'code', 'city')
    list_filter = ('is_active', 'city')
