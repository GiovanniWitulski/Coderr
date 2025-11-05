"""
URL routing for the 'orders_app' API.

Uses a DefaultRouter to automatically generate CRUD routes for the
OrderViewSet and adds custom paths for the order count views.
"""

from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderCountView, CompletedOrderCountView
from django.urls import path

# Initialize the router
router = DefaultRouter()

# Register the OrderViewSet. This creates:
# - /api/orders/ (list, create)
# - /api/orders/{id}/ (retrieve, update, partial_update, destroy)
router.register(r'orders', OrderViewSet, basename='order')

# Combine the router-generated URLs with custom paths
urlpatterns = router.urls + [
    # Custom path for counting in-progress orders
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    # Custom path for counting completed orders
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
]