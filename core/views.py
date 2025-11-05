"""
Core API Views
Provides global API views for the Coderr project.
"""

# 3rd-party Imports
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

# Local App Imports
from offers_app.models import Offer
from reviews_app.models import Review
from user_profile_app.models import UserProfile

class BaseInfoView(APIView):
    """
    Provides a public, read-only endpoint for platform-wide statistics.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request by querying and aggregating platform data.
        """

        # Perform aggregate queries
        review_count = Review.objects.count()
        business_profile_count = UserProfile.objects.filter(type=UserProfile.UserType.BUSINESS).count()
        offer_count = Offer.objects.count()
        avg_rating_data = Review.objects.aggregate(avg_rating=Avg('rating'))
        average_rating = avg_rating_data.get('avg_rating')

        # Handle null case if no reviews exist
        if average_rating is None:
            average_rating = 0.0
        else:
            average_rating = round(average_rating, 1)

        # Assemble response data
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }
        
        return Response(data, status=status.HTTP_200_OK)