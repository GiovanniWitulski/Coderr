from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from offers_app.models import Offer
from reviews_app.models import Review
from user_profile_app.models import UserProfile

@api_view(['GET'])
@permission_classes([AllowAny])
def base_info_view(request):
    review_count = Review.objects.count()
    business_profile_count = UserProfile.objects.filter(type=UserProfile.UserType.BUSINESS).count()
    offer_count = Offer.objects.count()

    avg_rating_data = Review.objects.aggregate(avg_rating=Avg('rating'))
    average_rating = avg_rating_data.get('avg_rating')

    if average_rating is None:
        average_rating = 0.0
    else:
        average_rating = round(average_rating, 1)

    data = {
        "review_count": review_count,
        "average_rating": average_rating,
        "business_profile_count": business_profile_count,
        "offer_count": offer_count
    }
    
    return Response(data, status=status.HTTP_200_OK)