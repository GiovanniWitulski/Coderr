from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from user_profile_app.models import UserProfile
from ..models import Review

def create_user_and_profile(username, user_type):
    user = User.objects.create_user(username=username, password='password')
    profile = UserProfile.objects.create(user=user, type=user_type)
    return user, profile

class ReviewAPITests(APITestCase):

    def setUp(self):
        self.business_user, self.business_profile = create_user_and_profile('business_user', 'business')
        self.customer_user, self.customer_profile = create_user_and_profile('customer_user', 'customer')

    def test_customer_can_create_review(self):
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('review-list') 
        
        data = {
            "business_user": self.business_profile.id,
            "rating": 5,
            "description": "Hervorragender Service, sehr zu empfehlen!"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertEqual(review.reviewer, self.customer_profile)
        self.assertEqual(review.business_user, self.business_profile)
        self.assertEqual(review.rating, 5)

        self.assertEqual(response.data['rating'], 5)
        self.assertEqual(response.data['description'], "Hervorragender Service, sehr zu empfehlen!")
        self.assertEqual(response.data['business_user'], self.business_profile.id)
        self.assertEqual(response.data['reviewer'], self.customer_profile.id)