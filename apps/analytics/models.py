from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel, Branch


class DailySalesSnapshot(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='daily_sales_snapshots')
    date = models.DateField(db_index=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_gross_sales = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    total_discounts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_tax_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_net_sales = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    # Channel breakdowns
    dine_in_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    takeaway_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Tender breakdowns
    cash_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    upi_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    card_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_daily_sales_snapshots'
        verbose_name = 'Daily Sales Snapshot'
        verbose_name_plural = 'Daily Sales Snapshots'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'date'], name='unique_branch_daily_snapshot')
        ]
        indexes = [
            models.Index(fields=['branch', 'date']),
        ]

    def __str__(self):
        return f"{self.branch.name} - {self.date}: ₹{self.total_net_sales} ({self.total_orders} orders)"


class MonthlySalesSnapshot(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='monthly_sales_snapshots')
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_monthly_sales_snapshots'
        verbose_name = 'Monthly Sales Snapshot'
        verbose_name_plural = 'Monthly Sales Snapshots'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'year', 'month'], name='unique_branch_monthly_snapshot')
        ]

    def __str__(self):
        return f"{self.branch.name} - {self.month:02d}/{self.year}: Rev ₹{self.total_revenue}"


class ProductSalesAnalytics(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='product_analytics')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, related_name='sales_analytics')
    date = models.DateField(db_index=True)
    quantity_sold = models.PositiveIntegerField(default=0)
    revenue_generated = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cost_of_goods_sold = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    gross_margin = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_product_sales_analytics'
        verbose_name = 'Product Sales Analytic'
        verbose_name_plural = 'Product Sales Analytics'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'menu_item', 'date'], name='unique_branch_item_date_analytics')
        ]

    def __str__(self):
        return f"{self.menu_item.name} at {self.branch.name} ({self.date}): {self.quantity_sold} sold (₹{self.revenue_generated})"


class CustomerAnalytics(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='customer_analytics')
    date = models.DateField(db_index=True)
    new_customers_count = models.PositiveIntegerField(default=0)
    repeat_customers_count = models.PositiveIntegerField(default=0)
    average_visit_interval_days = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    churn_risk_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'df_customer_analytics'
        verbose_name = 'Customer Analytic'
        verbose_name_plural = 'Customer Analytics'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'date'], name='unique_branch_customer_analytics_date')
        ]

    def __str__(self):
        return f"Customer metrics for {self.branch.name} on {self.date}"


class InventoryAnalytics(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory_analytics')
    date = models.DateField(db_index=True)
    total_stock_value = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    waste_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    consumption_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    stock_turnover_ratio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_inventory_analytics'
        verbose_name = 'Inventory Analytic'
        verbose_name_plural = 'Inventory Analytics'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'date'], name='unique_branch_inventory_analytics_date')
        ]

    def __str__(self):
        return f"Inventory metrics for {self.branch.name} on {self.date}: Valuation ₹{self.total_stock_value}"


class ExpenseAnalytics(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='expense_analytics')
    category = models.ForeignKey('expenses.ExpenseCategory', on_delete=models.CASCADE, related_name='analytics')
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_expense_analytics'
        verbose_name = 'Expense Analytic'
        verbose_name_plural = 'Expense Analytics'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'category', 'year', 'month'], name='unique_branch_exp_cat_month')
        ]

    def __str__(self):
        return f"{self.category.name} at {self.branch.name} ({self.month:02d}/{self.year}): ₹{self.total_amount}"


class ProfitAnalytics(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='profit_analytics')
    date = models.DateField(db_index=True)
    gross_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    cogs = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    operating_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    net_profit = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    profit_margin_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_profit_analytics'
        verbose_name = 'Profit Analytic'
        verbose_name_plural = 'Profit Analytics'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'date'], name='unique_branch_profit_analytics_date')
        ]

    def __str__(self):
        return f"Profit for {self.branch.name} on {self.date}: Net ₹{self.net_profit} ({self.profit_margin_percent}%)"


class DemandPrediction(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='demand_predictions')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, related_name='demand_predictions')
    prediction_date = models.DateField(db_index=True)
    predicted_quantity = models.PositiveIntegerField()
    confidence_low = models.PositiveIntegerField(default=0)
    confidence_high = models.PositiveIntegerField(default=0)
    generated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_demand_predictions'
        verbose_name = 'Demand Prediction'
        verbose_name_plural = 'Demand Predictions'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'menu_item', 'prediction_date'], name='unique_branch_item_prediction_date')
        ]

    def __str__(self):
        return f"Prediction for {self.menu_item.name} at {self.branch.name} on {self.prediction_date}: {self.predicted_quantity} units"
