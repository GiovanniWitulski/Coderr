"""
Serializers for the 'reviews_app'.

Defines how Review model instances are converted to JSON for API responses
and how JSON payloads are converted back into model instances.
"""

from rest_framework import serializers
from ..models import Review
from user_profile_app.models import UserProfile

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes the Review model.
    
    - `reviewer` is set automatically from the request context (read-only).
    - `business_user` is a writable field expecting the ID of a business profile.
    - Validates uniqueness to prevent duplicate reviews.
    """

    # 'reviewer' is read-only because it's set automatically based on
    # the logged-in user in the create method, not sent in the payload.
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    # 'business_user' is a writeable field. We specify a queryset
    # to validate that the provided ID is a valid 'business' user.
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
        """
        Validates uniqueness, considering both create and update operations.
        """
        
        reviewer = self.context['request'].user.profile
        business_user = data.get('business_user')

        if not business_user and self.instance:
            return data
        
        if not business_user and not self.instance:
             return data

        query = Review.objects.filter(business_user=business_user, reviewer=reviewer)

        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise serializers.ValidationError("You have already submitted a review for this provider.")
            
        return data

    def create(self, validated_data):
        # Inject the reviewer profile from the request context into the data
        validated_data['reviewer'] = self.context['request'].user.profile
        
        # Call the parent class's create method to save the object
        return super().create(validated_data)