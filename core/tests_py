from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_profile_app.models import UserProfile
from offers_app.models import Offer
from reviews_app.models import Review

def create_user_and_profile(username, user_type):
    from django.contrib.auth.models import User
    user = User.objects.create_user(username=username, password='password')
    profile = UserProfile.objects.create(user=user, type=user_type)
    return user, profile

class BaseInfoAPITest(APITestCase):

    def setUp(self):
        _, self.business1 = create_user_and_profile('business1', 'business')
        _, self.business2 = create_user_and_profile('business2', 'business')
        _, self.customer1 = create_user_and_profile('customer1', 'customer')

        Offer.objects.create(creator=self.business1, title="Angebot 1")
        Offer.objects.create(creator=self.business1, title="Angebot 2")
        Offer.objects.create(creator=self.business2, title="Angebot 3")

        Review.objects.create(business_user=self.business1, reviewer=self.customer1, rating=4, description="...")
        Review.objects.create(business_user=self.business2, reviewer=self.customer1, rating=5, description="...")
        
    def test_get_base_info(self):
        url = reverse('base-info') 

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "review_count": 2,
            "average_rating": 4.5, 
            "business_profile_count": 2,
            "offer_count": 3
        }
        
        self.assertEqual(response.data, expected_data)