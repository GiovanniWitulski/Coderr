from rest_framework import serializers
from ..models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'offer_type', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features']

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'creator', 'title', 'description', 'image', 'details', 'created_at', 'updated_at']
        extra_kwargs = {
            'creator': {'read_only': True}
        }

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
    
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
            
        return offer