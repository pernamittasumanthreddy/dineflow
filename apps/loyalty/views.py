"""Loyalty Program, Tier Tracking, and Points Redemption Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.loyalty.models import LoyaltyAccount, LoyaltyTransaction, LoyaltyTier
from apps.accounts.decorators import module_permission_required

@login_required
def loyalty_dashboard_view(request):
    """Overview of active loyalty accounts, tier distribution, and recent transactions."""
    accounts = LoyaltyAccount.objects.all().select_related('customer').order_by('-points_balance')[:50]
    recent_transactions = LoyaltyTransaction.objects.all().select_related('account__customer')[:25]
    
    tier_counts = {
        'platinum': LoyaltyAccount.objects.filter(current_tier=LoyaltyTier.PLATINUM).count(),
        'gold': LoyaltyAccount.objects.filter(current_tier=LoyaltyTier.GOLD).count(),
        'silver': LoyaltyAccount.objects.filter(current_tier=LoyaltyTier.SILVER).count(),
        'bronze': LoyaltyAccount.objects.filter(current_tier=LoyaltyTier.BRONZE).count(),
    }

    return render(request, 'loyalty/dashboard.html', {
        'accounts': accounts,
        'recent_transactions': recent_transactions,
        'tier_counts': tier_counts,
    })
