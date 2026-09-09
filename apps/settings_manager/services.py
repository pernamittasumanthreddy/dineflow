"""Global Configuration Key-Value Cache & Switch Retrieval Services."""
from apps.settings_manager.models import SystemSetting

_SETTINGS_CACHE = {}

def get_setting(key, default=None):
    """
    Retrieves system setting value by key with memory cache.
    """
    global _SETTINGS_CACHE
    if key in _SETTINGS_CACHE:
        return _SETTINGS_CACHE[key]

    try:
        setting = SystemSetting.objects.get(key=key)
        _SETTINGS_CACHE[key] = setting.value
        return setting.value
    except SystemSetting.DoesNotExist:
        return default

def set_setting(key, value, description=""):
    """
    Sets or updates system setting and updates cache.
    """
    global _SETTINGS_CACHE
    setting, _ = SystemSetting.objects.update_or_create(
        key=key,
        defaults={'value': str(value), 'description': description}
    )
    _SETTINGS_CACHE[key] = str(value)
    return setting

def clear_settings_cache():
    """Clears in-memory settings cache."""
    global _SETTINGS_CACHE
    _SETTINGS_CACHE.clear()

def get_thermal_printer_width():
    """Returns configured POS printer width in millimeters (80 or 58)."""
    val = get_setting('THERMAL_PRINTER_WIDTH_MM', default='80')
    try:
        return int(val)
    except (ValueError, TypeError):
        return 80
