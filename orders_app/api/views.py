from rest_framework import viewsets, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from .serializers import OrderSerializer

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.type == 'customer'
        )

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser]

    def get_queryset(self):
        return Order.objects.none()