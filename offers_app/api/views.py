"""
API Views for the 'offers_app'.

Provides the viewsets for:
- OfferViewSet: Full CRUD for Offer objects.
- OfferDetailViewSet: Read-only access for OfferDetail objects.
"""

from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from offers_app.api.filters import OfferFilter
from offers_app.api.permissions import IsOwnerOrReadOnly, IsBusinessUser
from ..models import Offer, OfferDetail
from .serializers import OfferDetailSerializer, OfferSerializer
from .pagination import StandardResultsSetPagination 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from django.db.models import Min


class OfferViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD (Create, Retrieve, Update, Delete) for Offers.
    Permissions are handled dynamically based on the action.
    """

    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination 

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    filterset_class = OfferFilter 
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']

    def get_queryset(self):
        return Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        ).all().order_by('-updated_at')

    def list(self, request, *args, **kwargs):
        """
        Lists all offers with explicit filter validation.
        """

        queryset = self.get_queryset()
        filterset = self.filterset_class(request.GET, queryset=queryset, request=request)
        
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
            
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        """
        Dynamically assigns permissions based on the request action.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsBusinessUser]
        elif self.action == 'list':
            permission_classes = [AllowAny]
        else:
            # Default for 'retrieve' and any custom actions
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
    permission_classes = [permissions.IsAuthenticated]