"""
API Views for the 'user_profile_app'.
Handles all logic for authentication.
"""

from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, mixins
from ..models import UserProfile
from .serializers import LoginSerializer, UserProfileSerializer, RegistrationSerializer
from rest_framework import generics
from .permissions import IsOwner

class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    Provides `retrieve` and `update` functionality for UserProfiles.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # Use the 'user' (user_id) from the URL for lookup, not the profile's 'id'.
    lookup_field = 'user'

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else: 
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class RegistrationView(APIView):
    """
    Handles new user registration via a POST request to /api/registration/.
    """
    permission_classes = [permissions.AllowAny] # Anyone can register.

    def post(self, request, *args, **kwargs):
        """
        Validates registration data, creates a new User and UserProfile,
        and returns an authentication token.
        """

        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # Use the aliased AuthToken
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    """
    Handles user login via a POST request to /api/login/.
    """

    permission_classes = [permissions.AllowAny] # Anyone can log in.

    def post(self, request, *args, **kwargs):
        """
        Validates user credentials and returns an authentication token.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Use the aliased AuthToken
            token, _ = Token.objects.get_or_create(user=user)

            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BusinessProfileListView(generics.ListAPIView):
    """
    Provides a read-only list of all profiles with the type 'business'.
    """

    queryset = UserProfile.objects.filter(type=UserProfile.UserType.BUSINESS).order_by('user__username')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class CustomerProfileListView(generics.ListAPIView):
    """
    Provides a read-only list of all profiles with the type 'customer'.
    """

    queryset = UserProfile.objects.filter(type=UserProfile.UserType.CUSTOMER).order_by('user__username')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None