from django.contrib import admin

from .models import (
    DailySalesSnapshot,
    DemandPrediction,
    MonthlySalesSnapshot,
    ProductSalesAnalytics,
    ProfitAnalytics,
)


@admin.register(DailySalesSnapshot)
class DailySalesSnapshotAdmin(admin.ModelAdmin):
    list_display = ['branch', 'date', 'total_orders', 'total_net_sales', 'dine_in_sales', 'delivery_sales', 'avg_order_value']
    list_filter = ['branch', 'date']


@admin.register(MonthlySalesSnapshot)
class MonthlySalesSnapshotAdmin(admin.ModelAdmin):
    list_display = ['branch', 'month', 'year', 'total_orders', 'total_revenue', 'net_profit']
    list_filter = ['branch', 'year', 'month']


@admin.register(ProductSalesAnalytics)
class ProductSalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'branch', 'date', 'quantity_sold', 'revenue_generated', 'gross_margin']
    list_filter = ['branch', 'date']
    search_fields = ['menu_item__name']


@admin.register(ProfitAnalytics)
class ProfitAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'date', 'gross_revenue', 'cogs', 'operating_expenses', 'net_profit', 'profit_margin_percent']
    list_filter = ['branch', 'date']


@admin.register(DemandPrediction)
class DemandPredictionAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'branch', 'prediction_date', 'predicted_quantity', 'confidence_low', 'confidence_high']
    list_filter = ['branch', 'prediction_date']
