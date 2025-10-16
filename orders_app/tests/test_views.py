from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from user_profile_app.models import UserProfile
from offers_app.models import Offer, OfferDetail
from ..models import Order

def create_user_and_profile(username, password, user_type):
    user = User.objects.create_user(username=username, password=password)
    profile = UserProfile.objects.create(user=user, type=user_type)
    return user, profile

class OrderAPITests(APITestCase):

    def setUp(self):
        self.business_user, self.business_profile = create_user_and_profile(
            'business_user', 'testpass123', 'business'
        )
        self.customer_user, self.customer_profile = create_user_and_profile(
            'customer_user', 'testpass123', 'customer'
        )

        self.offer = Offer.objects.create(
            creator=self.business_profile,
            title='Webdesign Service'
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type=OfferDetail.OfferType.PREMIUM,
            title='Premium package',
            delivery_time_in_days=10,
            price=1500.00,
            features=['Responsive Design', 'CMS']
        )

    def test_create_order_by_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('order-list')
        data = {'offer_detail_id': self.offer_detail.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.customer, self.customer_profile)
        self.assertEqual(order.business, self.business_profile)
        self.assertEqual(order.total_price, self.offer_detail.price)
        self.assertEqual(order.status, Order.Status.IN_PROGRESS)

        self.assertEqual(response.data['title'], 'Premium package')
        self.assertEqual(response.data['status'], 'in_progress')
        # Die Doku gibt User-IDs zurück, nicht die Profil-IDs. Wir prüfen gegen die User-ID.
        self.assertEqual(response.data['customer_user'], self.customer_user.id) 
        self.assertEqual(response.data['business_user'], self.business_user.id)