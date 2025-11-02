from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import UserProfile

class UserAuthAPITests(APITestCase):

    def setUp(self):
        self.registration_url = reverse('registration')

        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongPassword123!",
            "repeated_password": "strongPassword123!",
            "type": "customer"
        }

    def test_user_registration_success(self):
        response = self.client.post(self.registration_url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.profile.type, "customer")

        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], "testuser")
        self.assertEqual(response.data['user_id'], user.id)

    def test_registration_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['repeated_password'] = 'wrongPassword'

        response = self.client.post(self.registration_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)