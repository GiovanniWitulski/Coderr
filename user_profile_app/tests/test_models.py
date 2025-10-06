from django.test import TestCase
from django.contrib.auth.models import User
from ..models import UserProfile

class UserProfileModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='test@example.com'
        )

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(
            user=self.user,
            type=UserProfile.UserType.BUSINESS,
            location='Berlin',
            tel='123456789'
        )
        
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.type, 'business')
        self.assertEqual(profile.location, 'Berlin')
        self.assertEqual(self.user.profile, profile)

    def test_user_profile_defaults(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.type, UserProfile.UserType.CUSTOMER)
        
        self.assertEqual(profile.location, '')
        self.assertEqual(profile.tel, '')
        self.assertEqual(profile.description, '')
        self.assertEqual(profile.working_hours, '')
        self.assertIsNone(profile.file.name)

    def test_str_method(self):
        customer_profile = UserProfile.objects.create(
            user=self.user, 
            type=UserProfile.UserType.CUSTOMER
        )
        expected_customer_str = f"{self.user.username} - Customer"
        self.assertEqual(str(customer_profile), expected_customer_str)

        business_user = User.objects.create_user(username='businessuser', password='password123')
        business_profile = UserProfile.objects.create(
            user=business_user,
            type=UserProfile.UserType.BUSINESS
        )
        expected_business_str = f"{business_user.username} - Business"
        self.assertEqual(str(business_profile), expected_business_str)

    def test_on_delete_cascade(self):
        UserProfile.objects.create(user=self.user)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.user.delete()
        self.assertEqual(UserProfile.objects.count(), 0)