"""Expenses Django Admin."""
from django.contrib import admin
from apps.expenses.models import ExpenseCategory, Expense

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'branch', 'category', 'amount', 'payment_mode', 'expense_date', 'is_approved')
    list_filter = ('branch', 'category', 'payment_mode', 'is_approved', 'expense_date')
    search_fields = ('title', 'notes')
