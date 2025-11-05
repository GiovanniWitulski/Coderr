"""
API Views for the 'offers_app'.

Provides the viewsets for:
- OfferViewSet: Full CRUD for Offer objects.
- OfferDetailViewSet: Read-only access for OfferDetail objects.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from offers_app.api.permissions import IsOwnerOrReadOnly, IsBusinessUser
from ..models import Offer, OfferDetail
from .serializers import OfferDetailSerializer, OfferSerializer
from rest_framework import permissions


class OfferViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD (Create, Retrieve, Update, Delete) for Offers.
    Permissions are handled dynamically based on the action.
    """

    # Default sorting is newest 'updated_at' first.
    queryset = Offer.objects.all().order_by('-updated_at')
    serializer_class = OfferSerializer
    
    def get_permissions(self):
        """
        Dynamically assigns permissions based on the request action.
        """

        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsBusinessUser]
        elif self.action in ['list', 'retrieve']: 
            permission_classes = [AllowAny]
        else:
            # Fallback to a safe default (must be authenticated)
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Overrides the create behavior to automatically assign the logged-in
        user's profile as the 'creator' of the new offer.
        """

        serializer.save(creator=self.request.user.profile)


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only endpoints (`list` and `retrieve`) for OfferDetails.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    # Set to AllowAny to accommodate frontend client behavior
    permission_classes = [permissions.AllowAny]