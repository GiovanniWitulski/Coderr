from rest_framework import permissions

class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'business'
        )

class IsOwnerOfOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.profile or obj.business == request.user.profile