"""
Data models for the 'reviews_app'.

This module defines the Review model, which represents a single review
submitted by a 'customer' user for a 'business' user.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user_profile_app.models import UserProfile

class Review(models.Model):
    """
    Represents a single review a customer leaves for a business.
    Ensures that one customer can only leave one review per business
    via the `unique_together` constraint in the Meta class.
    """

    # The business user who is being reviewed.
    business_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_received', # All reviews a business has received
        limit_choices_to={'type': UserProfile.UserType.BUSINESS}
    )
    
    # The customer user who is writing the review.
    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_written', # All reviews a customer has written
        limit_choices_to={'type': UserProfile.UserType.CUSTOMER}
    )
    
    # The rating score, restricted to 1-5 stars.
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # The text content of the review.
    description = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        """Returns a readable string representation of the review."""
        return f"Review from {self.reviewer.user.username} for {self.business_user.user.username} ({self.rating} stars)"