"""
API Views for the 'reviews_app'.
Provides the ReviewViewSet for full CRUD functionality on Review models.
"""

from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomerUser, IsReviewOwner
from .filters import ReviewFilter

class ReviewViewSet(mixins.CreateModelMixin,   
                   mixins.ListModelMixin,     
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,   
                   mixins.DestroyModelMixin,  
                   viewsets.GenericViewSet):
    """
    Provides full CRUD for Reviews with dynamic, action-based permissions.
    """

    # Add default ordering to prevent UnorderedObjectListWarning
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def get_permissions(self):
        """
        Dynamically assigns permissions based on the request action.
        """

        if self.action == 'create':
            # Only authenticated customers can create reviews
            permission_classes = [IsAuthenticated, IsCustomerUser] 
        elif self.action in ['update', 'partial_update', 'destroy']:
            #Only the review owner can modify.
            permission_classes = [IsAuthenticated, IsReviewOwner]
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]