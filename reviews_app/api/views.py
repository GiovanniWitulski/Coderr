# reviews_app/api/views.py

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated 
from ..models import Review
from .serializers import ReviewSerializer
from .permissions import IsCustomerUser

class ReviewViewSet(mixins.CreateModelMixin,   
                   mixins.ListModelMixin,     
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,   
                   mixins.DestroyModelMixin,  
                   viewsets.GenericViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsCustomerUser] 
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
            
        return [permission() for permission in permission_classes]