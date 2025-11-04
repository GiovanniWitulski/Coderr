from django.urls import path
from .views import BusinessProfileListView, CustomerProfileListView, RegistrationView, LoginView
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = router.urls + [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),

    path('profiles/business/', BusinessProfileListView.as_view(), name='profiles-business'),
    path('profiles/customer/', CustomerProfileListView.as_view(), name='profiles-customer'),
]