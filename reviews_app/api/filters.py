from django_filters import rest_framework as filters
from ..models import Review
#import the Review model from models.py

class ReviewFilter(filters.FilterSet):
    business_user_id = filters.NumberFilter(field_name='business_user__id')
    reviewer_id = filters.NumberFilter(field_name='reviewer__id')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']