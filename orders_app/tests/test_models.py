# orders_app/tests/test_model.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import ProtectedError

from user_profile_app.models import UserProfile
from offers_app.models import Offer, OfferDetail 
from orders_app.models import Order 

class OrderModelTest(TestCase):
    def setUp(self):
        self.business_user = User.objects.create_user(username='business', password='password')
        self.customer_user = User.objects.create_user(username='customer', password='password')

        self.business_profile = UserProfile.objects.create(
            user=self.business_user,
            type=UserProfile.UserType.BUSINESS
        )

        self.customer_profile = UserProfile.objects.create(
            user=self.customer_user,
            type=UserProfile.UserType.CUSTOMER
        )

        self.offer = Offer.objects.create(
            creator=self.business_profile,
            title='Webdesign Service'
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type=OfferDetail.OfferType.PREMIUM,
            title='Premium Paket',
            delivery_time_in_days=10,
            price=1500.00
        )

    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.customer_profile,
            offer_detail=self.offer_detail,
            business=self.business_profile,
            total_price=self.offer_detail.price 
        )

        self.assertEqual(order.customer, self.customer_profile)
        self.assertEqual(order.offer_detail, self.offer_detail)
        self.assertEqual(order.business, self.business_profile)
        self.assertEqual(order.total_price, 1500.00)
        self.assertEqual(order.status, Order.Status.IN_PROGRESS)

        expected_str = f"Order {order.id} by {self.customer_user.username} for {self.offer_detail.title}"
        self.assertEqual(str(order), expected_str)

    def test_on_delete_cascade_for_offer_detail(self):
        order = Order.objects.create(
            customer=self.customer_profile,
            offer_detail=self.offer_detail,
            business=self.business_profile,
            total_price=self.offer_detail.price
        )
        
        order_count_before = Order.objects.count()
        self.assertEqual(order_count_before, 1)
        self.offer_detail.delete()

        order_count_after = Order.objects.count()
        self.assertEqual(order_count_after, 0)


    def test_on_delete_cascade_for_customer(self):
        order = Order.objects.create(
            customer=self.customer_profile,
            offer_detail=self.offer_detail,
            business=self.business_profile,
            total_price=self.offer_detail.price
        )

        order_count_before = Order.objects.count()
        self.assertEqual(order_count_before, 1)
        self.customer_profile.delete()
        
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_after, 0)