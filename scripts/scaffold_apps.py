import os

apps = [
    'core', 'employees', 'menu', 'tables', 'orders', 'kitchen',
    'inventory', 'suppliers', 'purchases', 'billing', 'payments',
    'customers', 'delivery', 'offers', 'loyalty', 'reviews',
    'expenses', 'taxes', 'notifications', 'analytics', 'ml',
    'reports', 'audit', 'settings_app'
]

for app in apps:
    path = os.path.join('apps', app)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, '__init__.py'), 'w', encoding='utf-8') as f:
        pass
    class_name = ''.join(word.title() for word in app.split('_')) + 'Config'
    display_name = app.replace('_', ' ').title()
    with open(os.path.join(path, 'apps.py'), 'w', encoding='utf-8') as f:
        f.write(f'''from django.apps import AppConfig


class {class_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
    verbose_name = '{display_name}'
''')

print("All 24 app modules scaffolded successfully.")
