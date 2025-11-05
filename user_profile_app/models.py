"""
Data models for the 'user_profile_app'.

This module defines the UserProfile model, which extends Django's
built-in User model to include a user type (Customer/Business)
and other profile-specific information.
"""

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extends the default Django User model with app-specific fields.
    """

    class UserType(models.TextChoices):
        """Enumeration for the two types of users on the platform."""
        BUSINESS = 'business', 'Business'
        CUSTOMER = 'customer', 'Customer'

    # The core link to Django's authentication User model.
    # related_name='profile' allows access via `user.profile`.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # The role of the user on the platform.
    type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    
    # Profile-specific fields
    file = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=30, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the string representation of the profile."""
        return f"{self.user.username} - {self.get_type_display()}"