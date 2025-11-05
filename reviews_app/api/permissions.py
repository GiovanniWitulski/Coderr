from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'customer'
        )
    
class IsReviewerOwner(permissions.BasePermission):
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