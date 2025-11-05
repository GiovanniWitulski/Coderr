"""
Data models for the 'offers_app'.

This module defines the database structure for:
- Offer: The main service listing created by a business user.
- OfferDetail: The specific pricing tiers (Basic, Standard, Premium)
  associated with a single Offer.
"""

from django.db import models
from user_profile_app.models import UserProfile

# Create your models here.
    
class Offer(models.Model):
    """
    Represents a service offer created by a business user.
    """
    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='offers'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the string representation of the model, which is the title."""
        return self.title


class OfferDetail(models.Model):
    """
    Represents a specific pricing tier (Basic, Standard, Premium)
    for a parent Offer.
    """
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='details'
    )

    class OfferType(models.TextChoices):
        """Enumeration for the different tiers of an offer."""
        BASIC = 'basic', 'Basic'
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

    offer_type = models.CharField(
        max_length=20,
        choices=OfferType.choices,
    )

    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(null=True, blank=True)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)

    def __str__(self):
        """Returns a string representation (e.g., 'Website Design - Premium')."""
        return f"{self.offer.title} - {self.title}"