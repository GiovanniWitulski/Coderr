"""
Serializers for the 'offers_app'.
Defines how Offer and OfferDetail models are converted to and from JSON.
"""

from rest_framework import serializers
from ..models import Offer, OfferDetail

class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializes OfferDetail fields for nested use within OfferSerializer
    and for its own 'offerdetails' endpoint.
    """
    class Meta:
        model = OfferDetail
        # Define the fields to include in the JSON output
        fields = ['id', 'offer_type', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features']

class OfferSerializer(serializers.ModelSerializer):
    """
    This serializer handles the nested creation of OfferDetails when an
    Offer is created.
    """

    # This field represents the nested list of OfferDetails.
    # It uses OfferDetailSerializer and expects a list.
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'creator', 'title', 'description', 'image', 'details', 'created_at', 'updated_at']
        extra_kwargs = {
            # 'creator' is set automatically by the view (perform_create),
            'creator': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Overrides the default create method to handle nested 'details'.
        """

        # Pop the 'details' data off the validated data
        details_data = validated_data.pop('details')

        # Create the main Offer object
        offer = Offer.objects.create(**validated_data)
    
        # Loop through the details and create OfferDetail objects
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
            
        return offer