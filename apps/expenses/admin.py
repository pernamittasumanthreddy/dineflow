from django.contrib import admin

from .models import Expense, ExpenseApproval, ExpenseAttachment, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'restaurant', 'is_active']
    list_filter = ['restaurant', 'is_active']


class ExpenseAttachmentInline(admin.TabularInline):
    model = ExpenseAttachment
    extra = 0


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'title', 'branch', 'category', 'total_amount', 'expense_date', 'status']
    list_filter = ['branch', 'category', 'status', 'expense_date']
    search_fields = ['expense_number', 'title', 'vendor_name']
    inlines = [ExpenseAttachmentInline]


@admin.register(ExpenseApproval)
class ExpenseApprovalAdmin(admin.ModelAdmin):
    list_display = ['expense', 'approver', 'status', 'approved_at']
    list_filter = ['status', 'approved_at']
