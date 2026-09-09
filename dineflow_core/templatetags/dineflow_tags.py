"""
Custom Template Tags and Filters for DineFlow Indian Restaurant ERP.
"""
from django import template
import re

register = template.Library()

@register.filter(name='inr')
def inr_format(value):
    """
    Format numeric values to Indian Rupee currency format (e.g., ₹1,25,000.00).
    """
    if value is None or value == '':
        return '₹0.00'
    try:
        val = float(value)
    except (ValueError, TypeError):
        return f"₹{value}"
    
    is_negative = val < 0
    val = abs(val)
    
    # Split integer and decimal parts
    parts = f"{val:.2f}".split('.')
    integer_part = parts[0]
    decimal_part = parts[1]
    
    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        # Group remaining digits by 2s from the right
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three
        
    result = f"₹{formatted}.{decimal_part}"
    return f"-{result}" if is_negative else result

@register.filter(name='status_class')
def status_class(status):
    """
    Returns semantic CSS classes for badges according to Indian Restaurant ERP state.
    """
    if not status:
        return 'badge-neutral'
    s = str(status).lower().replace(' ', '_').replace('-', '_')
    
    mapping = {
        'active': 'badge-success',
        'available': 'badge-success',
        'paid': 'badge-success',
        'completed': 'badge-success',
        'ready': 'badge-info',
        'served': 'badge-success',
        'in_stock': 'badge-success',
        'delivered': 'badge-success',
        'confirmed': 'badge-success',
        'approved': 'badge-success',
        'present': 'badge-success',
        'on_time': 'badge-success',
        
        'preparing': 'badge-warning',
        'pending': 'badge-warning',
        'occupied': 'badge-warning',
        'reserved': 'badge-warning',
        'low_stock': 'badge-warning',
        'in_transit': 'badge-warning',
        'review': 'badge-warning',
        'half_day': 'badge-warning',
        'late': 'badge-warning',
        
        'urgent': 'badge-danger',
        'cancelled': 'badge-danger',
        'out_of_stock': 'badge-danger',
        'expired': 'badge-danger',
        'failed': 'badge-danger',
        'absent': 'badge-danger',
        'void': 'badge-danger',
        'unpaid': 'badge-danger',
        'overdue': 'badge-danger',
        
        'cleaning': 'badge-secondary',
        'inactive': 'badge-secondary',
        'draft': 'badge-secondary',
        'hold': 'badge-secondary',
    }
    return mapping.get(s, 'badge-neutral')

@register.filter(name='diet_badge')
def diet_badge(tag):
    """
    Returns dietary icon/badge class for Indian food classification.
    """
    if not tag:
        return 'veg-mark'
    t = str(tag).lower()
    if 'non' in t:
        return 'nonveg-mark'
    elif 'egg' in t:
        return 'egg-mark'
    elif 'jain' in t:
        return 'jain-mark'
    return 'veg-mark'
