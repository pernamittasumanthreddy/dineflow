import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('SECRET_KEY', 'dineflow-insecure-prod-ready-restaurant-erp-key-2026')

DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Third-party
    'rest_framework',

    # DineFlow Modular Architecture
    'apps.core.apps.CoreConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.restaurants.apps.RestaurantsConfig',
    'apps.branches.apps.BranchesConfig',
    'apps.employees.apps.EmployeesConfig',
    'apps.attendance.apps.AttendanceConfig',
    'apps.shifts.apps.ShiftsConfig',
    'apps.payroll.apps.PayrollConfig',
    'apps.menu.apps.MenuConfig',
    'apps.tables.apps.TablesConfig',
    'apps.reservations.apps.ReservationsConfig',
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
    'apps.tax.apps.TaxConfig',
    'apps.refunds.apps.RefundsConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.sales.apps.SalesConfig',
    'apps.analytics.apps.AnalyticsConfig',
    'apps.ml_prediction.apps.MlPredictionConfig',
    'apps.reports.apps.ReportsConfig',
    'apps.audit.apps.AuditConfig',
    'apps.settings_manager.apps.SettingsManagerConfig',
    'apps.backups.apps.BackupsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.audit.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'apps.core.context_processors.dineflow_global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TIMEOUT': 20,
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization & Internationalization
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
DEFAULT_CURRENCY = 'INR'
DEFAULT_CURRENCY_SYMBOL = '₹'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Reports & ML Models directories
REPORTS_DIR = BASE_DIR / 'generated_reports'
ML_MODELS_DIR = BASE_DIR / 'ml_models'
BACKUPS_DIR = BASE_DIR / 'backups_archive'

for directory in [REPORTS_DIR, ML_MODELS_DIR, BACKUPS_DIR, BASE_DIR / 'static', BASE_DIR / 'media']:
    directory.mkdir(parents=True, exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session and Auth configuration
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
SESSION_COOKIE_AGE = 86400  # 24 Hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'dineflow': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
