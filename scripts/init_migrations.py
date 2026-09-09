import os

apps = [
    'core', 'employees', 'menu', 'tables', 'orders', 'kitchen',
    'inventory', 'suppliers', 'purchases', 'billing', 'payments',
    'customers', 'delivery', 'offers', 'loyalty', 'reviews',
    'expenses', 'taxes', 'notifications', 'analytics', 'ml',
    'reports', 'audit', 'settings_app'
]

for app in apps:
    mig_dir = os.path.join('apps', app, 'migrations')
    os.makedirs(mig_dir, exist_ok=True)
    init_file = os.path.join(mig_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w', encoding='utf-8') as f:
            pass

print("Migration directories initialized for all apps.")
