"""
Serializers for the 'orders_app'.
Defines how Order model instances are converted to JSON for API responses
and how JSON payloads are converted into model instances.
"""

from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes Order objects.
    """

    # --- Read-only fields for GET responses ---
    # These fields are populated from the related OfferDetail model.
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)

    # --- Write-only field for POST requests ---
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(), 
        source='offer_detail',  # This links 'offer_detail_id' to the 'offer_detail' model field 
        write_only=True         # This field is only used for creating/writing, not for reading
    )

    # These fields read from the related User model (via UserProfile).
    customer_user = serializers.IntegerField(source='customer.user.id', read_only=True)
    business_user = serializers.IntegerField(source='business.user.id', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions', 
            'delivery_time_in_days', 'price', 'features', 'offer_type', 
            'status', 'created_at', 'updated_at', 'offer_detail_id'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """
        Overrides the default create method to auto-populate order details.
        """

        offer_detail = validated_data.get('offer_detail')

        # Get the customer's profile from the request (passed by the view)
        customer_profile = self.context['request'].user.profile

        # Get the business owner from the offer
        business_profile = offer_detail.offer.creator

        # Create the order
        order = Order.objects.create(
            offer_detail=offer_detail,
            customer=customer_profile,
            business=business_profile,
            total_price=offer_detail.price # Set the price from the offer detail
        )
        return order

    def update(self, instance, validated_data):
        """
        Overrides the default update method to restrict updates.
        """
        
        # Only update the 'status' field.
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance