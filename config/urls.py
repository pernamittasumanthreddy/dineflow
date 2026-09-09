"""DineFlow Master URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core Dashboard & Home
    path('', include('apps.core.urls', namespace='core')),
    
    # Domain Applications
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('restaurants/', include('apps.restaurants.urls', namespace='restaurants')),
    path('branches/', include('apps.branches.urls', namespace='branches')),
    path('employees/', include('apps.employees.urls', namespace='employees')),
    path('attendance/', include('apps.attendance.urls', namespace='attendance')),
    path('shifts/', include('apps.shifts.urls', namespace='shifts')),
    path('payroll/', include('apps.payroll.urls', namespace='payroll')),
    path('menu/', include('apps.menu.urls', namespace='menu')),
    path('tables/', include('apps.tables.urls', namespace='tables')),
    path('reservations/', include('apps.reservations.urls', namespace='reservations')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('kitchen/', include('apps.kitchen.urls', namespace='kitchen')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('suppliers/', include('apps.suppliers.urls', namespace='suppliers')),
    path('purchases/', include('apps.purchases.urls', namespace='purchases')),
    path('billing/', include('apps.billing.urls', namespace='billing')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('customers/', include('apps.customers.urls', namespace='customers')),
    path('delivery/', include('apps.delivery.urls', namespace='delivery')),
    path('offers/', include('apps.offers.urls', namespace='offers')),
    path('loyalty/', include('apps.loyalty.urls', namespace='loyalty')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('expenses/', include('apps.expenses.urls', namespace='expenses')),
    path('tax/', include('apps.tax.urls', namespace='tax')),
    path('refunds/', include('apps.refunds.urls', namespace='refunds')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('sales/', include('apps.sales.urls', namespace='sales')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('ml_prediction/', include('apps.ml_prediction.urls', namespace='ml_prediction')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
    path('settings/', include('apps.settings_manager.urls', namespace='settings_manager')),
    path('backups/', include('apps.backups.urls', namespace='backups')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom HTTP Error Handlers
handler400 = 'apps.core.views.bad_request_view'
handler403 = 'apps.core.views.permission_denied_view'
handler404 = 'apps.core.views.page_not_found_view'
handler500 = 'apps.core.views.server_error_view'
