"""
Data models for the 'orders_app'.

This module defines the Order model, which represents a transaction
between a customer and a business for a specific OfferDetail.
"""

from django.db import models
from user_profile_app.models import UserProfile

# Create your models here.

class Order(models.Model):
    """
    Represents a single order placed by a customer for a business's offer.
    """

    class Status(models.TextChoices):
        """Enumeration for the possible states of an order."""

        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    # Foreign key to the specific offer tier being purchased.
    offer_detail = models.ForeignKey(
        'offers_app.OfferDetail',
        on_delete=models.CASCADE, # If the offer detail is deleted, the order is also deleted.
        related_name='orders'
    )

    # The customer who placed the order.
    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        limit_choices_to={'type': UserProfile.UserType.CUSTOMER},
    )

    # The business user who owns the offer and is fulfilling the order.
    business = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='business_orders',
        limit_choices_to={'type': UserProfile.UserType.BUSINESS},
    )

    # Timestamps
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Order status
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )
    
    # Auto-managed timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns a readable string representation of the order."""
        return f"Order {self.id} by {self.customer.user.username} for {self.offer_detail.title}"