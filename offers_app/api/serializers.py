"""
Serializers for the 'offers_app'.
Defines how Offer and OfferDetail models are converted to and from JSON.
"""

from rest_framework import serializers

from user_profile_app.models import UserProfile
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

class OfferDetailUrlSerializer(serializers.ModelSerializer):
    """
    Serializes just the ID and URL for an OfferDetail,
    used in read-only list/retrieve views.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetail-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes basic, read-only user information.
    """

    # 'source' accesses the related User object
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username']

class OfferListRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for READ operations (list, retrieve) on Offers.
    Uses OfferDetailUrlSerializer to display details as URLs.
    """
    
    # Displays details as hyperlinks instead of full nested objects
    details = OfferDetailUrlSerializer(many=True, read_only=True)
    
    user = serializers.ReadOnlyField(source='creator.id')
    user_details = UserDetailsSerializer(source='creator', read_only=True)

    # SerializerMethodFields for calculated or annotated values
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image', 'details', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        """
        Returns the minimum price. 
        """

        if hasattr(obj, 'min_price') and obj.min_price is not None:
            return obj.min_price
        aggregate = obj.details.aggregate(min_price=Min('price'))
        return aggregate.get('min_price')

    def get_min_delivery_time(self, obj):
        """
        Returns the minimum delivery time.
        """

        if hasattr(obj, 'min_delivery_time') and obj.min_delivery_time is not None:
            return obj.min_delivery_time
        
        # Fallback: Manual aggregation
        aggregate = obj.details.aggregate(min_time=Min('delivery_time_in_days'))
        return aggregate.get('min_time')
    
class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for WRITE operations (create, update) on Offers.
    Uses the full OfferDetailSerializer for nested writes.
    """
    
    # Uses the full detail serializer for nested writes
    details = OfferDetailSerializer(many=True)
    user = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image', 'details', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate(self, data):
        """
        Ensures that 'offer_type' is provided when updating 'details',
        as it is used as the key to identify which detail to update.
        """

        # 'self.instance' is present on updates (PATCH/PUT), but not on create (POST)
        if self.instance and 'details' in data:
            for detail in data['details']:
                # 'offer_type' is used as the lookup-key in the update() method
                if 'offer_type' not in detail:
                    raise serializers.ValidationError(
                        {"details": "The 'offer_type' must be provided to update details."}
                    )
        return data

    def create(self, validated_data):
        """
        Creates an 'Offer' and its associated 'OfferDetail' objects nested.
        """

        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        # Create all detail objects sent in the payload
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    
    def update(self, instance, validated_data):
        """
        Updates an 'Offer' and its associated 'OfferDetail' objects.
        """

        details_data = validated_data.pop('details', None)

        # Update the main instance (Offer)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        #  Update nested details (OfferDetail)
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type:
                    try:
                        # Find the existing detail
                        detail_to_update = instance.details.get(offer_type=offer_type)

                        # Update the found detail
                        for key, value in detail_data.items():
                            setattr(detail_to_update, key, value)
                        detail_to_update.save()
                    except OfferDetail.DoesNotExist:
                        # If detail doesn't exist, nothing happens
                        pass
        return instance