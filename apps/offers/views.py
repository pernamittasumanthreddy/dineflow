"""Promotions, Coupon Codes, and Discount Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from django.utils import timezone
from apps.offers.models import Offer, DiscountType
from apps.accounts.decorators import module_permission_required

@login_required
def offer_list_view(request):
    """Marketing promotions and discount vouchers."""
    offers = Offer.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'offers/offer_list.html', {'offers': offers})

@login_required
def validate_coupon_api(request):
    """AJAX endpoint validating coupon codes and returning discount amount."""
    code = request.GET.get('code', '').strip().upper()
    subtotal = Decimal(request.GET.get('subtotal', '0.00'))
    
    offer = Offer.objects.filter(code=code, is_active=True).first()
    if not offer or not offer.is_valid_now:
        return JsonResponse({'valid': False, 'message': 'Invalid or expired coupon code.'})
        
    if subtotal < offer.min_order_amount:
        return JsonResponse({'valid': False, 'message': f'Minimum order amount of ₹{offer.min_order_amount} required.'})

    discount = Decimal('0.00')
    if offer.discount_type == DiscountType.PERCENTAGE:
        discount = (subtotal * (offer.discount_value / Decimal('100.00'))).quantize(Decimal('0.01'))
        if offer.max_discount_amount and discount > offer.max_discount_amount:
            discount = offer.max_discount_amount
    else:
        discount = min(offer.discount_value, subtotal)

    return JsonResponse({
        'valid': True,
        'code': offer.code,
        'title': offer.title,
        'discount_amount': float(discount),
        'message': f'Coupon applied! ₹{discount} saved.'
    })
