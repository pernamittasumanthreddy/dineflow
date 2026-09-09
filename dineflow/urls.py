from django.contrib import admin
from django.urls import path, include

# Customize Admin Site Branding
admin.site.site_header = "DineFlow Restaurant ERP & Database Portal"
admin.site.site_title = "DineFlow ERP"
admin.site.index_title = "DineFlow Enterprise Database & Management System"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core Modular Apps
    path('', include('apps.landing.urls', namespace='landing')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('pos/', include('apps.pos.urls', namespace='pos')),
    path('kds/', include('apps.kds.urls', namespace='kds')),
    path('tables/', include('apps.tables.urls', namespace='tables')),
    path('menu/', include('apps.menu.urls', namespace='menu')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('suppliers/', include('apps.suppliers.urls', namespace='suppliers')),
    path('billing/', include('apps.billing.urls', namespace='billing')),
    path('hr/', include('apps.hr.urls', namespace='hr')),
    path('crm/', include('apps.crm.urls', namespace='crm')),
    path('delivery/', include('apps.delivery.urls', namespace='delivery')),
    path('expenses/', include('apps.expenses.urls', namespace='expenses')),
    path('tax-mgmt/', include('apps.tax_mgmt.urls', namespace='tax_mgmt')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('settings/', include('apps.settings_app.urls', namespace='settings_app')),
    path('restaurants/', include('apps.restaurants.urls', namespace='restaurants')),
    path('branches/', include('apps.branches.urls', namespace='branches')),
]

handler404 = 'apps.accounts.views.custom_404_view'
handler500 = 'apps.accounts.views.custom_500_view'
handler403 = 'apps.accounts.views.custom_403_view'
