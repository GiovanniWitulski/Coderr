"""
Custom permission classes for the 'reviews_app'.
These classes are used in the ReviewViewSet to control who can
create, edit, or delete reviews.
"""

from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow 'customer' type users to perform
    write actions.
    """

    def has_permission(self, request, view):
        """
        Checks if the method is safe, or if the user is an
        authenticated 'customer'.
        """

        # Allow read-only methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check for write permissions.
        # User must be authenticated and have a profile of type 'customer'.
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'customer'
        )
    
class IsReviewOwner(permissions.BasePermission):
    """
    Object-level permission to only allow the creator (reviewer) of
    a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the request.user's profile matches the review's reviewer.
        """

        # Write permissions are only allowed to the reviewer of the object.
        return obj.reviewer == request.user.profile