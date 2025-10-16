from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from user_profile_app.models import UserProfile
from ..models import Review

def create_user_and_profile(username, user_type):
    user = User.objects.create_user(username=username, password='password')
    profile = UserProfile.objects.create(user=user, type=user_type)
    return profile

class ReviewModelTest(TestCase):
    def setUp(self):
        self.business_profile = create_user_and_profile('business_user', 'business')
        self.customer_profile = create_user_and_profile('customer_user', 'customer')

    def test_review_creation(self):
        review = Review.objects.create(
            business_user=self.business_profile,
            reviewer=self.customer_profile,
            rating=5,
            description="good service"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.business_user, self.business_profile)
        self.assertEqual(review.reviewer, self.customer_profile)
        self.assertEqual(str(review), "Review from customer_user for business_user (5 stars)")

    def test_rating_validator(self):
        with self.assertRaises(ValidationError):
            review_low = Review(business_user=self.business_profile, reviewer=self.customer_profile, rating=0, description="to low")
            review_low.full_clean()

        with self.assertRaises(ValidationError):
            review_high = Review(business_user=self.business_profile, reviewer=self.customer_profile, rating=6, description="too high")
            review_high.full_clean()

    def test_unique_together_constraint(self):
        Review.objects.create(
            business_user=self.business_profile,
            reviewer=self.customer_profile,
            rating=4,
            description="first review"
        )

        with self.assertRaises(IntegrityError):
            Review.objects.create(
                business_user=self.business_profile,
                reviewer=self.customer_profile,
                rating=5,
                description="second review"
            )