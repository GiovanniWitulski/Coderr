from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from offers_app.api.permissions import IsOwnerOrReadOnly
from ..models import Offer
from .serializers import OfferSerializer

class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated and hasattr(request.user, 'profile') and 
            request.user.profile.type == 'business')

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsBusinessUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.profile)