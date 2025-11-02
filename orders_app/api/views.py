from rest_framework import viewsets, permissions, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from ..models import Order
from .serializers import OrderSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from user_profile_app.models import UserProfile
from django.db.models import Q
from .permissions import IsBusinessUser, IsOwnerOfOrder

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
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,   
                   mixins.DestroyModelMixin,  
                   viewsets.GenericViewSet):
    
    serializer_class = OrderSerializer
    pagination_class = None
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
             return Order.objects.none() 
        user_profile = self.request.user.profile
        return Order.objects.filter(
            Q(customer=user_profile) | Q(business=user_profile)
        ).distinct()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsCustomerUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsBusinessUser, IsOwnerOfOrder]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
            
        return [permission() for permission in permission_classes]
    

class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        try:
            UserProfile.objects.get(id=business_user_id, type=UserProfile.UserType.BUSINESS)
            count = Order.objects.filter(
                business_id=business_user_id, 
                status=Order.Status.IN_PROGRESS
            ).count()
            return Response({"order_count": count}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)


class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        try:
            UserProfile.objects.get(id=business_user_id, type=UserProfile.UserType.BUSINESS)
            count = Order.objects.filter(
                business_id=business_user_id, 
                status=Order.Status.COMPLETED
            ).count()
            return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)