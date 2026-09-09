"""Custom Template Filters for DineFlow ERP."""
from django import template
from django.utils.safestring import mark_safe
from apps.core.utils import format_inr

register = template.Library()

@register.filter(name='inr')
def inr_filter(value):
    """Format numeric values as INR currency string."""
    return format_inr(value)

@register.filter(name='status_badge')
def status_badge(status):
    """Return a styled badge HTML for various statuses."""
    status_str = str(status).upper()
    badge_classes = {
        'AVAILABLE': 'badge-success',
        'COMPLETED': 'badge-success',
        'CONFIRMED': 'badge-info',
        'PAID': 'badge-success',
        'ACTIVE': 'badge-success',
        'OCCUPIED': 'badge-danger',
        'PREPARING': 'badge-warning',
        'PENDING': 'badge-warning',
        'RESERVED': 'badge-info',
        'CLEANING': 'badge-secondary',
        'MAINTENANCE': 'badge-dark',
        'CANCELLED': 'badge-danger',
        'REFUNDED': 'badge-secondary',
        'OVERDUE': 'badge-danger',
        'LOW_STOCK': 'badge-danger',
    }
    css_class = badge_classes.get(status_str, 'badge-primary')
    return mark_safe(f'<span class="badge {css_class}">{status_str}</span>')

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
