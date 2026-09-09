"""
Django settings for DineFlow - Enterprise Restaurant ERP & Management System.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dineflow-enterprise-erp-secret-key-prod-ready-2026'

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'core.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # DineFlow ERP Domain Apps
    'apps.core.apps.CoreConfig',
    'apps.restaurants.apps.RestaurantsConfig',
    'apps.branches.apps.BranchesConfig',
    'apps.employees.apps.EmployeesConfig',
    'apps.customers.apps.CustomersConfig',
    'apps.menu.apps.MenuConfig',
    'apps.tables.apps.TablesConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.kitchen.apps.KitchenConfig',
    'apps.inventory.apps.InventoryConfig',
    'apps.suppliers.apps.SuppliersConfig',
    'apps.purchases.apps.PurchasesConfig',
    'apps.billing.apps.BillingConfig',
    'apps.payments.apps.PaymentsConfig',
    'apps.delivery.apps.DeliveryConfig',
    'apps.offers.apps.OffersConfig',
    'apps.loyalty.apps.LoyaltyConfig',
    'apps.reviews.apps.ReviewsConfig',
    'apps.expenses.apps.ExpensesConfig',
    'apps.taxes.apps.TaxesConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.analytics.apps.AnalyticsConfig',
    'apps.ml.apps.MlConfig',
    'apps.reports.apps.ReportsConfig',
    'apps.audit.apps.AuditConfig',
    'apps.settings_app.apps.SettingsAppConfig',

    # UI Portals & Role View Modules
    'apps.landing',
    'apps.accounts',
    'apps.dashboard',
    'apps.pos',
    'apps.kds',
    'apps.crm',
    'apps.hr',
    'apps.tax_mgmt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.accounts.middleware.RBACAuthMiddleware',
]

LOGIN_URL = '/accounts/role-select/'
LOGIN_REDIRECT_URL = '/dashboard/owner/'
LOGOUT_REDIRECT_URL = '/accounts/role-select/'


ROOT_URLCONF = 'dineflow_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dineflow_core.context_processors.dineflow_global_context',
            ],
            'libraries': {
                'dineflow_tags': 'dineflow_core.templatetags.dineflow_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'dineflow_core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization & Localization for India
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Backup Directory Configuration
BACKUP_DIR = BASE_DIR / 'backups'
BACKUP_DIR.mkdir(exist_ok=True)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
