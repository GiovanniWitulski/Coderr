"""
URL routing for the 'user_profile_app' API.
Registers all endpoints related to users, profiles, and auth.
"""

from django.urls import path
from .views import BusinessProfileListView, CustomerProfileListView, RegistrationView, LoginView
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

# Use a router for the ViewSet
router = DefaultRouter()
# Registers /api/profile/{user_id}/ (for retrieve, update)
router.register(r'profile', UserProfileViewSet, basename='profile')

# Combine router URLs with custom paths for APIViews
urlpatterns = router.urls + [
    # Auth endpoints
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),

    # Profile list endpoints
    path('profiles/business/', BusinessProfileListView.as_view(), name='profiles-business'),
    path('profiles/customer/', CustomerProfileListView.as_view(), name='profiles-customer'),
]