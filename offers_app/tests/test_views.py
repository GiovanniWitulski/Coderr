from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from user_profile_app.models import UserProfile
from ..models import Offer

# Die Hilfsfunktion von vorhin
def create_user_and_profile(username, password, user_type):
    user = User.objects.create_user(username=username, password=password)
    profile = UserProfile.objects.create(user=user, type=user_type)
    return user, profile

class OfferCreateAPITests(APITestCase):

    def setUp(self):
        self.business_user, self.business_profile = create_user_and_profile(
            'business_user', 'testpass123', 'business'
        )

    def test_create_offer_as_business_user(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offer-list') 
        
        offer_data = {
            "title": "Professionelles Logo-Design",
            "description": "Einzigartiges Logo für Ihre Marke.",
            "details": [
                {"offer_type": "basic", "title": "Basic", "delivery_time_in_days": 5, "price": 150, "features": ["1 Konzept"]},
                {"offer_type": "standard", "title": "Standard", "delivery_time_in_days": 4, "price": 300, "features": ["3 Konzepte", "Vektordatei"]},
                {"offer_type": "premium", "title": "Premium", "delivery_time_in_days": 3, "price": 500, "features": ["5 Konzepte", "Vektordatei", "Social Media Kit"]}
            ]
        }
        
        response = self.client.post(url, offer_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(Offer.objects.first().title, "Professionelles Logo-Design")
        self.assertEqual(Offer.objects.first().details.count(), 3)