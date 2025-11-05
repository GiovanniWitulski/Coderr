"""
API Views for the 'orders_app'.

Provides:
- OrderViewSet: Full CRUD for Order objects with dynamic permissions.
- OrderCountView: Endpoint to count 'in_progress' orders for a business.
- CompletedOrderCountView: Endpoint to count 'completed' orders for a business.
"""

# 3rd-party Imports
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny 
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.db.models import Q

# Local Imports
from ..models import Order
from .serializers import OrderSerializer
from user_profile_app.models import UserProfile
from .permissions import IsBusinessUser, IsOwnerOfOrder, IsCustomerUser

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,   
                   mixins.DestroyModelMixin,  
                   viewsets.GenericViewSet):
    """
    Provides full CRUD for Orders with dynamic, action-based permissions.
    """
    
    serializer_class = OrderSerializer
    pagination_class = None
    
    def get_queryset(self):
        """
        Dynamically filters the queryset based on the logged-in user.
        """

        # Return nothing if the user isn't logged in
        if not self.request.user.is_authenticated:
             return Order.objects.none() 
        user_profile = self.request.user.profile
        # Use Q objects to filter with an OR condition
        return Order.objects.filter(
            Q(customer=user_profile) | Q(business=user_profile)
        ).distinct()

    def get_permissions(self):
        """
        Assigns the correct permission class based on the current action.
        """

        if self.action == 'create':
            # Only authenticated customers can create orders
            permission_classes = [IsAuthenticated, IsCustomerUser]
        elif self.action in ['update', 'partial_update']:
            # Only the authenticated business owner of the order can update
            permission_classes = [IsAuthenticated, IsBusinessUser, IsOwnerOfOrder]
        elif self.action == 'destroy':
            # Only admin users can delete
            permission_classes = [IsAdminUser]
        else: # 'list' and 'retrieve' actions
            permission_classes = [AllowAny]
            
        return [permission() for permission in permission_classes]
    

class OrderCountView(APIView):
    """
    Provides a read-only endpoint to get the count of 'in_progress'
    orders for a specific business user.
    """

    permission_classes = [IsAuthenticated] # Only authenticated users can see counts

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Handles the GET request for counting in-progress orders.
        Validates the business_user_id and returns the count.
        """

        try:
            # Validate that the ID belongs to a real business user
            UserProfile.objects.get(id=business_user_id, type=UserProfile.UserType.BUSINESS)
            # Filter orders by business_id and status
            count = Order.objects.filter(
                business_id=business_user_id, 
                status=Order.Status.IN_PROGRESS
            ).count()
            return Response({"order_count": count}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            # Catches invalid ID formats
            return Response({"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)


class CompletedOrderCountView(APIView):
    """
    Provides a read-only endpoint to get the count of 'completed'
    orders for a specific business user.
    """

    permission_classes = [IsAuthenticated] # Only authenticated users can see counts

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Handles the GET request for counting completed orders.
        Validates the business_user_id and returns the count.
        """
        try:
            # Validate that the ID belongs to a real business user
            UserProfile.objects.get(id=business_user_id, type=UserProfile.UserType.BUSINESS)
            # Filter orders by business_id and status
            count = Order.objects.filter(
                business_id=business_user_id, 
                status=Order.Status.COMPLETED
            ).count()
            return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            # Catches invalid ID formats 
            return Response({"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)
        