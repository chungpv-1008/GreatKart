from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, OrderViewSet, PaymentViewSet, ShippingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'products', ProductViewSet, basename="product")
router.register(r'orders', OrderViewSet, basename="order")
router.register(r'payments', PaymentViewSet, basename="payment")
router.register(r'shipping', ShippingViewSet, basename="shipping")
urlpatterns = [
    path('', include(router.urls)),
]