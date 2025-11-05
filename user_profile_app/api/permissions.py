"""
Custom permission classes for the 'user_profile_app'.
"""

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permission to only allow the owner of a
    profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user associated with the UserProfile
        is the same as the user making the request.
        """
        
        # Read permissions are handled by the view's get_permissions method.
        return obj.user == request.user