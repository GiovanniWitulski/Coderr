"""
Serializers for the 'offers_app'.
Defines how Offer and OfferDetail models are converted to and from JSON.
"""

from rest_framework import serializers
from ..models import Offer, OfferDetail
from django.db.models import Min

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

    user = serializers.ReadOnlyField(source='creator.id')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image', 'details', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']
        extra_kwargs = {
            # 'user' (-> creator) is set automatically by the view (perform_create),
            'user': {'read_only': True}
        }

    def get_min_price(self, obj):
        if hasattr(obj, 'min_price') and obj.min_price is not None:
            return obj.min_price
        aggregate = obj.details.aggregate(min_price=Min('price'))
        return aggregate.get('min_price')

    def get_min_delivery_time(self, obj):
        if hasattr(obj, 'min_delivery_time') and obj.min_delivery_time is not None:
            return obj.min_delivery_time
        aggregate = obj.details.aggregate(min_time=Min('delivery_time_in_days'))
        return aggregate.get('min_time')
    
    def validate(self, data):
        if self.instance and 'details' in data:
            for detail in data['details']:
                if 'offer_type' not in detail:
                    raise serializers.ValidationError(
                        {"details": "The 'offer_type' must be provided to update details."}
                    )
        return data

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
    
    def update(self, instance, validated_data):
        """
        Overrides the default update method to handle nested 'details' update.
        """
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type:
                    try:
                        detail_to_update = instance.details.get(offer_type=offer_type)
                        for key, value in detail_data.items():
                            setattr(detail_to_update, key, value)
                        detail_to_update.save()
                    except OfferDetail.DoesNotExist:
                        pass
        return instance