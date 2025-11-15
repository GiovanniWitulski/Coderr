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
        Validates the uniqueness of the (reviewer, business_user) pair.

        This method ensures that a user (reviewer) can only submit one review
        for a specific business_user. It correctly handles both 'create' (POST) 
        and 'update' (PUT/PATCH) operations.
        """

        # Get the reviewer from the authenticated user's profile
        reviewer = self.context['request'].user.profile
        
        # Determine the 'business_user' being reviewed.
        if self.instance:
            # This is a PATCH/PUT (Update) operation.
            business_user = data.get('business_user', self.instance.business_user)
        else:
            # This is a POST (Create) operation.
            business_user = data.get('business_user')

        # The PrimaryKeyRelatedField should already prevent 'None' on POST,
        # but we add this check for extra safety.
        if not business_user and not self.instance:
            raise serializers.ValidationError(
                {"business_user": "This field is required."}
            )

        # Perform the uniqueness check:
        # Has this 'reviewer' already submitted a review for this 'business_user'?
        query = Review.objects.filter(
            business_user=business_user, 
            reviewer=reviewer
        )

        if self.instance:
            # On update, exclude the object itself from the check.
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            # If the query returns any results, a review already exists.
            raise serializers.ValidationError(
                "You have already submitted a review for this provider."
            )
            
        return data

    def create(self, validated_data):
        # Inject the reviewer profile from the request context into the data
        validated_data['reviewer'] = self.context['request'].user.profile
        
        # Call the parent class's create method to save the object
        return super().create(validated_data)