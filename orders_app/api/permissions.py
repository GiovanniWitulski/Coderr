"""
Permission classes for the 'orders_app'.
These classes define who can access or modify order-related resources.
"""

from rest_framework import permissions

class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow users with a 'business' profile
    to perform an action.
    """

    def has_permission(self, request, view):
        """
        Checks if the user is authenticated and is a 'business' user.
        """

        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'business'
        )

class IsOwnerOfOrder(permissions.BasePermission):
    """
    Permission to only allow the customer or
    the business user associated with the order to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the request.user's profile is either the customer
        or the business on the order object.
        """
        
        # obj is the Order instance
        return obj.customer == request.user.profile or obj.business == request.user.profile
    

class IsCustomerUser(permissions.BasePermission):
    """
    Permission to only allow 'customer' type users to perform
    write actions (like creating an order).
    """

    def has_permission(self, request, view):
        # Allow read-only method
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check for write permissions:
        # User must be authenticated and have a profile of type 'customer'.
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.type == 'customer'
        )