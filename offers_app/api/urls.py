"""
URL routing for the 'offers_app' API.
Uses a DefaultRouter to automatically generate routes:
"""

from rest_framework.routers import DefaultRouter
from .views import OfferDetailViewSet, OfferViewSet

# Create a router instance
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailViewSet, basename='offerdetail')

# The router.urls list contains all the generated URL patterns
urlpatterns = router.urls