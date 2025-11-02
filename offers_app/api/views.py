from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from offers_app.api.permissions import IsOwnerOrReadOnly, IsBusinessUser
from ..models import Offer, OfferDetail
from .serializers import OfferDetailSerializer, OfferSerializer
from rest_framework import permissions


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-updated_at')
    serializer_class = OfferSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'create':
            permission_classes = [IsBusinessUser]
        elif self.action in ['list', 'retrieve']: 
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.profile)


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.AllowAny]