from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(), source='offer_detail', write_only=True
    )

    customer_user = serializers.IntegerField(source='customer.user.id', read_only=True)
    business_user = serializers.IntegerField(source='business.user.id', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions', 
            'delivery_time_in_days', 'price', 'features', 'offer_type', 
            'status', 'created_at', 'updated_at', 'offer_detail_id'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']

    def create(self, validated_data):
        offer_detail = validated_data.get('offer_detail')
        customer_profile = self.context['request'].user.profile
        business_profile = offer_detail.offer.creator

        order = Order.objects.create(
            offer_detail=offer_detail,
            customer=customer_profile,
            business=business_profile,
            total_price=offer_detail.price
        )
        return order