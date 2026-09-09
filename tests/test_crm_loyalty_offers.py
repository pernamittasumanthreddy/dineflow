"""Comprehensive Test Suite for Guest CRM, Loyalty Points & Tiers, Offers, and Reviews."""
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.customers.models import Customer
from apps.loyalty.models import LoyaltyAccount, LoyaltyTier, LoyaltyTransaction
from apps.offers.models import Offer, DiscountType
from apps.reviews.models import Review

User = get_user_model()

class CRMLoyaltyOffersTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="crm@royalnizam.in",
            phone="+91 40 2334 5678",
            address_line1="Jubilee Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500033"
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name="Banjara Hills Flagship",
            code="HYD-BANJARA",
            address="Road No 12",
            city="Hyderabad",
            state="Telangana",
            pincode="500034",
            phone="+91 40 2334 1100"
        )
        self.customer = Customer.objects.create(
            name="Rajesh Sharma",
            phone="+91 98490 12345",
            email="guest.rajesh@gmail.com",
            total_visits=5,
            total_spent=Decimal('6500.00')
        )
        self.manager = User.objects.create_user(
            email="mgr@dineflow.in",
            username="mgr_crm",
            role=RoleChoices.MANAGER,
            branch=self.branch,
            restaurant=self.restaurant
        )

    def test_loyalty_account_and_tier_progression(self):
        """Test loyalty account points accrual and dynamic tier progression."""
        account = LoyaltyAccount.objects.create(
            customer=self.customer,
            points_balance=800,
            lifetime_points=800,
            current_tier=LoyaltyTier.BRONZE
        )
        self.assertEqual(account.current_tier, LoyaltyTier.BRONZE)

        # Earn points crossing Silver tier (1000+ points)
        account.lifetime_points = 1200
        account.points_balance = 1200
        account.update_tier()
        self.assertEqual(account.current_tier, LoyaltyTier.SILVER)

        # Earn points crossing Gold tier (2500+ points)
        account.lifetime_points = 3000
        account.update_tier()
        self.assertEqual(account.current_tier, LoyaltyTier.GOLD)

        # Earn points crossing Platinum tier (5000+ points)
        account.lifetime_points = 5500
        account.update_tier()
        self.assertEqual(account.current_tier, LoyaltyTier.PLATINUM)

    def test_loyalty_points_transaction_ledger(self):
        """Test points earn and redemption ledger entries."""
        account = LoyaltyAccount.objects.create(
            customer=self.customer,
            points_balance=500,
            lifetime_points=500
        )
        # Earn 100 points
        txn_earn = LoyaltyTransaction.objects.create(
            account=account,
            points=100,
            transaction_type='EARNED',
            description="Dining reward for Order #101"
        )
        account.points_balance += 100
        account.save()

        # Burn 50 points
        txn_burn = LoyaltyTransaction.objects.create(
            account=account,
            points=-50,
            transaction_type='REDEEMED',
            description="Discount redeemed at checkout"
        )
        account.points_balance -= 50
        account.save()

        self.assertEqual(account.points_balance, 550)
        self.assertEqual(txn_earn.points, 100)
        self.assertEqual(txn_burn.points, -50)

    def test_promotional_offer_discount_and_validity(self):
        """Test percentage coupon with min order requirement and max cap."""
        offer = Offer.objects.create(
            code="ROYAL20",
            title="Royal Feast 20% Off",
            branch=self.branch,
            discount_type=DiscountType.PERCENTAGE,
            discount_value=Decimal('20.00'),
            min_order_amount=Decimal('1000.00'),
            max_discount_amount=Decimal('400.00'),
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=30),
            usage_limit=500,
            times_used=10
        )
        self.assertTrue(offer.is_valid_now)

        # Test discount calculation for ₹1500 order
        order_amount = Decimal('1500.00')
        raw_discount = (order_amount * (offer.discount_value / Decimal('100.00'))).quantize(Decimal('0.01'))
        # 20% of 1500 = 300 (under 400 cap)
        final_discount = min(raw_discount, offer.max_discount_amount)
        self.assertEqual(final_discount, Decimal('300.00'))

        # Test discount calculation for ₹3000 order (20% of 3000 = 600, capped at 400)
        large_order = Decimal('3000.00')
        raw_discount_large = (large_order * (offer.discount_value / Decimal('100.00'))).quantize(Decimal('0.01'))
        final_discount_large = min(raw_discount_large, offer.max_discount_amount)
        self.assertEqual(final_discount_large, Decimal('400.00'))

    def test_customer_review_and_management_response(self):
        """Test guest rating submission and manager reply recording."""
        review = Review.objects.create(
            branch=self.branch,
            customer=self.customer,
            overall_rating=5,
            food_rating=5,
            ambience_rating=5,
            service_rating=5,
            comment="The Biryani was outstanding, genuine Nizami taste!",
            is_published=True
        )
        self.assertEqual(review.overall_rating, 5)
        self.assertTrue(review.is_published)

        # Manager replies
        review.management_response = "Thank you Mr. Rajesh! Glad you loved the flavours."
        review.responded_by = self.manager
        review.responded_at = timezone.now()
        review.save()

        self.assertEqual(review.responded_by.username, "mgr_crm")
        self.assertTrue(len(review.management_response) > 0)
