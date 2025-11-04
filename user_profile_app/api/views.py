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
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else: 
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
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
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
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
    queryset = UserProfile.objects.filter(type=UserProfile.UserType.BUSINESS).order_by('user__username')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class CustomerProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type=UserProfile.UserType.CUSTOMER).order_by('user__username')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None