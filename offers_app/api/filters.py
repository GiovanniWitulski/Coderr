from django_filters import rest_framework as filters
from ..models import Offer

class OfferFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')
    creator_id = filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Offer
        fields = ['min_price', 'max_delivery_time', 'creator_id']