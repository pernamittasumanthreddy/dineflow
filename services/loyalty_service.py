from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.loyalty.models import CustomerTier, LoyaltyAccount, LoyaltyTransaction, Reward, RewardRedemption
from apps.customers.models import Customer
from apps.orders.models import Order
from apps.audit.models import AuditLog


class LoyaltyService:
    @classmethod
    @transaction.atomic
    def get_or_create_loyalty_account(cls, customer: Customer) -> LoyaltyAccount:
        restaurant = customer.restaurant
        # Find lowest tier as default
        default_tier = CustomerTier.objects.filter(restaurant=restaurant).order_by('min_lifetime_spend').first()
        if not default_tier:
            default_tier = CustomerTier.objects.create(
                restaurant=restaurant,
                name='Bronze',
                min_lifetime_spend=Decimal('0.00'),
                points_multiplier=Decimal('1.00'),
                benefits_description='Standard member rewards'
            )

        account, _ = LoyaltyAccount.objects.get_or_create(
            customer=customer,
            defaults={'tier': default_tier, 'current_points': Decimal('0.00')}
        )
        return account

    @classmethod
    @transaction.atomic
    def process_order_loyalty(cls, order: Order, user=None):
        """
        Awards loyalty points upon bill completion based on customer's tier multiplier.
        Evaluates tier upgrade if lifetime spend threshold is crossed.
        """
        if not order.customer:
            return None

        customer = order.customer
        account = cls.get_or_create_loyalty_account(customer)
        tier = account.tier

        # Default rule: 1 point per ₹20 spent (5%), multiplied by tier multiplier
        base_points = (order.final_amount * Decimal('0.05')).quantize(Decimal('0.01'))
        awarded_points = (base_points * tier.points_multiplier).quantize(Decimal('0.01'))

        bal_before = account.current_points
        bal_after = bal_before + awarded_points

        account.current_points = bal_after
        account.lifetime_earned_points += awarded_points
        account.last_activity_date = timezone.now()

        # Update customer lifetime totals
        customer.total_spend += order.final_amount
        customer.total_visits += 1
        customer.loyalty_points = bal_after
        customer.save(update_fields=['total_spend', 'total_visits', 'loyalty_points', 'updated_at'])

        # Check for tier promotion
        next_tier = CustomerTier.objects.filter(
            restaurant=customer.restaurant,
            min_lifetime_spend__lte=customer.total_spend
        ).order_by('-min_lifetime_spend').first()

        if next_tier and next_tier != account.tier:
            account.tier = next_tier

        account.save(update_fields=['current_points', 'lifetime_earned_points', 'tier', 'last_activity_date', 'updated_at'])

        # Immutable ledger transaction
        LoyaltyTransaction.objects.create(
            account=account,
            order=order,
            transaction_type='EARNED',
            points=awarded_points,
            balance_before=bal_before,
            balance_after=bal_after,
            reason=f"Earned points for Order #{order.order_number} ({tier.name} Tier {tier.points_multiplier}x)"
        )

        return account

    @classmethod
    @transaction.atomic
    def redeem_reward(cls, customer: Customer, reward: Reward, order: Order = None, user=None) -> RewardRedemption:
        """
        Redeems a reward from loyalty points, ensuring atomic deduction and audit logging.
        """
        account = cls.get_or_create_loyalty_account(customer)
        points_cost = Decimal(str(reward.points_required))

        if account.current_points < points_cost:
            raise ValueError(f"Insufficient points. Required: {points_cost}, Available: {account.current_points}")

        bal_before = account.current_points
        bal_after = bal_before - points_cost

        account.current_points = bal_after
        account.lifetime_redeemed_points += points_cost
        account.last_activity_date = timezone.now()
        account.save(update_fields=['current_points', 'lifetime_redeemed_points', 'last_activity_date', 'updated_at'])

        customer.loyalty_points = bal_after
        customer.save(update_fields=['loyalty_points', 'updated_at'])

        # Immutable ledger transaction
        LoyaltyTransaction.objects.create(
            account=account,
            order=order,
            transaction_type='REDEEMED',
            points=-points_cost,
            balance_before=bal_before,
            balance_after=bal_after,
            reason=f"Redeemed for reward: {reward.title}"
        )

        redemption = RewardRedemption.objects.create(
            account=account,
            reward=reward,
            order=order,
            points_spent=reward.points_required,
            status='REDEEMED',
            redeemed_at=timezone.now()
        )

        AuditLog.objects.create(
            action='UPDATE',
            model_name='LoyaltyAccount',
            object_id=str(account.id),
            object_repr=str(account),
            user=user,
            changes={'points_deducted': [str(bal_before), str(bal_after)]}
        )

        return redemption
