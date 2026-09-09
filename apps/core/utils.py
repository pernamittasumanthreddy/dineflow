"""Core utilities for Indian currency formatting, numbers, and dates."""
from decimal import Decimal, ROUND_HALF_UP

def format_inr(amount):
    """
    Format a numeric amount into Indian Currency Format (Lakhs and Crores).
    Example: 125000.50 -> ₹1,25,000.50
    """
    if amount is None:
        return "₹0.00"
    
    dec = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    is_negative = dec < 0
    dec = abs(dec)
    
    parts = f"{dec:.2f}".split('.')
    integer_part = parts[0]
    decimal_part = parts[1]
    
    if len(integer_part) <= 3:
        formatted_int = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        
        chunks = []
        while len(remaining) > 2:
            chunks.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            chunks.insert(0, remaining)
            
        formatted_int = ",".join(chunks) + "," + last_three

    result = f"₹{'-' if is_negative else ''}{formatted_int}.{decimal_part}"
    return result

def round_inr(value):
    """Quantize to 2 decimal places using standard commercial rounding."""
    if value is None:
        return Decimal('0.00')
    return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calculate_gst_breakdown(subtotal, tax_rate_percent=Decimal('5.0'), is_interstate=False):
    """
    Calculate CGST, SGST, IGST from taxable subtotal.
    Restaurant food typically attracts 5% GST (2.5% CGST + 2.5% SGST).
    """
    subtotal = Decimal(str(subtotal))
    tax_rate = Decimal(str(tax_rate_percent)) / Decimal('100.0')
    total_tax = round_inr(subtotal * tax_rate)
    
    if is_interstate:
        cgst = Decimal('0.00')
        sgst = Decimal('0.00')
        igst = total_tax
    else:
        cgst = round_inr(total_tax / Decimal('2.0'))
        sgst = total_tax - cgst  # Ensure exact split without penny loss
        igst = Decimal('0.00')
        
    grand_total = subtotal + total_tax
    return {
        'subtotal': subtotal,
        'tax_rate_percent': tax_rate_percent,
        'cgst': cgst,
        'sgst': sgst,
        'igst': igst,
        'total_tax': total_tax,
        'grand_total': grand_total
    }
