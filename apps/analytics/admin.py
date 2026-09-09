"""Analytics Django Admin."""
from django.contrib import admin
from apps.analytics.models import DailyAnalyticsSnapshot

@admin.register(DailyAnalyticsSnapshot)
class DailyAnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ('date', 'branch', 'total_revenue', 'total_expenses', 'net_profit', 'order_count', 'revpash', 'table_turnover_rate')
    list_filter = ('branch', 'date')
