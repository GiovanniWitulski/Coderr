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
        Checks if the request user has permission to access the specific order object.
        """

        # Check if the user is either the customer or the business user associated with the order
        is_owner = obj.customer == request.user.profile or obj.business == request.user.profile

        # If the user is neither, deny access immediately
        if not is_owner:
            return False
        
        # Only 'business' profiles are allowed to update/patch the order
        if view.action in ['update', 'partial_update']:
            return request.user.profile.type == 'business'

        return True
    

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