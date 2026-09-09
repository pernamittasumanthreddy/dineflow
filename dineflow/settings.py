"""
Django settings for dineflow project.
Restaurant ERP & Management System - Database Architecture Implementation
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-!a@-^h$h#!9ew+1=ez!jfig)a%(rh#!m805^ift)4aogc!ib7&'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Custom User Model
AUTH_USER_MODEL = 'core.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party packages
    'rest_framework',
    'corsheaders',

    # DineFlow ERP Domain Apps
    'apps.core.apps.CoreConfig',
    'apps.employees.apps.EmployeesConfig',
    'apps.menu.apps.MenuConfig',
    'apps.tables.apps.TablesConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.kitchen.apps.KitchenConfig',
    'apps.inventory.apps.InventoryConfig',
    'apps.suppliers.apps.SuppliersConfig',
    'apps.purchases.apps.PurchasesConfig',
    'apps.billing.apps.BillingConfig',
    'apps.payments.apps.PaymentsConfig',
    'apps.customers.apps.CustomersConfig',
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
    'apps.accounts',
    'apps.landing',
    'apps.dashboard',
    'apps.pos',
    'apps.kds',
    'apps.crm',
    'apps.hr',
    'apps.tax_mgmt',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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

ROOT_URLCONF = 'dineflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
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

WSGI_APPLICATION = 'dineflow.wsgi.application'

# Database Configuration
# Supports SQLite for development and PostgreSQL for production
DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite').lower()

if DB_ENGINE == 'postgresql' or DB_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'dineflow_db'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'CONN_MAX_AGE': 60,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'TIMEOUT': 20,
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization - Localized for Indian ERP
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files and Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Backup Directory Configuration
BACKUP_DIR = BASE_DIR / 'backups'
BACKUP_DIR.mkdir(exist_ok=True)
