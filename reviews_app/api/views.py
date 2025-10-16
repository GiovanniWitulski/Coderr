from rest_framework import viewsets, permissions, mixins
from ..models import Review
from .serializers import ReviewSerializer

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'customer'
        )

class ReviewViewSet(mixins.CreateModelMixin,   
                    mixins.ListModelMixin,     
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin,   
                    mixins.DestroyModelMixin,  
                    viewsets.GenericViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]