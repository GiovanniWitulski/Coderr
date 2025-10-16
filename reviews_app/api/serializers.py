from rest_framework import serializers
from ..models import Review
from user_profile_app.models import UserProfile

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(type=UserProfile.UserType.BUSINESS),
    )

    class Meta:
        model = Review
        fields = [
            'id', 
            'business_user',
            'reviewer',
            'rating', 
            'description', 
            'created_at', 
            'updated_at'
        ]
    
    def validate(self, data):
        business_user = data.get('business_user')
        reviewer = self.context['request'].user.profile
        
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already submitted a review for this provider.")
            
        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user.profile
        
        return super().create(validated_data)