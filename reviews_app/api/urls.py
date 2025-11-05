"""
URL routing for the 'reviews_app' API.

Uses a DefaultRouter to automatically generate CRUD routes for
the ReviewViewSet.
"""

from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

# Initialize the router
router = DefaultRouter()

# Register the ReviewViewSet. This creates:
# - /api/reviews/ (list, create)
# - /api/reviews/{id}/ (retrieve, update, partial_update, destroy)
router.register(r'reviews', ReviewViewSet, basename='review')

# Expose the router-generated URLs
urlpatterns = router.urls