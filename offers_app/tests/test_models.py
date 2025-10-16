from django.test import TestCase
from django.contrib.auth.models import User
from user_profile_app.models import UserProfile
from ..models import Offer, OfferDetail
import time

def create_user_and_profile(username, type='business'):
    user = User.objects.create_user(username=username, password='password')
    profile = UserProfile.objects.create(user=user, type=type)
    return profile


class OfferModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.creator_profile = create_user_and_profile('test_creator')

    def test_offer_creation(self):
        offer = Offer.objects.create(
            creator=self.creator_profile,
            title="My first offer",
            description="test description"
        )
        self.assertEqual(offer.title, "My first offer")
        self.assertEqual(offer.creator.user.username, 'test_creator')
        self.assertIsNotNone(offer.created_at)
        self.assertIsNotNone(offer.updated_at)

    def test_offer_str_method(self):
        offer = Offer.objects.create(creator=self.creator_profile, title="Productname")
        self.assertEqual(str(offer), "Productname")


class OfferDetailModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        creator_profile = create_user_and_profile('detail_creator')
        cls.offer = Offer.objects.create(creator=creator_profile, title="parent offer")

    def test_offer_detail_creation(self):
        detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type='basic',
            title="Basic Package",
            delivery_time_in_days=7,
            price=99.99,
            features=["Feature 1", "Feature 2"]
        )
        self.assertEqual(detail.offer.title, "parent offer")
        self.assertEqual(detail.get_offer_type_display(), "Basic") 
        self.assertEqual(float(detail.price), 99.99)
        self.assertEqual(len(detail.features), 2)
        
    def test_offer_detail_str_method(self):
        detail = OfferDetail.objects.create(
            offer=self.offer,
            offer_type='premium',
            title="Premium Package",
            delivery_time_in_days=3,
            price=299.99
        )
        self.assertEqual(str(detail), "parent offer - Premium Package")

    def test_cascade_delete(self):
        OfferDetail.objects.create(offer=self.offer, offer_type='basic', title="Detail 1", delivery_time_in_days=1, price=10)
        OfferDetail.objects.create(offer=self.offer, offer_type='basic', title="Detail 2", delivery_time_in_days=2, price=20)
        
        self.assertEqual(OfferDetail.objects.count(), 2)
        self.offer.delete()
        self.assertEqual(OfferDetail.objects.count(), 0)