"""
Custom permission classes for the 'offers_app'.

This module defines permissions to control access based on user roles
(like 'business') or object ownership.
"""

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow owners of an object to edit or delete it.
    Read-only access (GET, HEAD, OPTIONS) is allowed for everyone.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the request method is safe or if the user is the creator.
        """

        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the 'creator' of the offer.
        return obj.creator == request.user.profile

class IsBusinessUser(permissions.BasePermission):
    """
    Permission to only allow 'business' type users to perform
    certain actions (like creating an offer).
    """
    def has_permission(self, request, view):
        # Allow read-only methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check for write permissions:
        # User must be authenticated and have a profile of type 'business'.
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'business'
        )