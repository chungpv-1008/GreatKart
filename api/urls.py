from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet, 
    OrderViewSet, 
    PaymentViewSet, 
    ShippingViewSet, 
    OrderCancelAPIView,
    CheckoutAPIView,
    MomoWebhookAPIView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'products', ProductViewSet, basename="product")
router.register(r'orders', OrderViewSet, basename="order")
router.register(r'payments', PaymentViewSet, basename="payment")
router.register(r'shipping', ShippingViewSet, basename="shipping")
urlpatterns = [
    path('', include(router.urls)),
    path(r'orders/cancel-order/<int:order_id>', OrderCancelAPIView.as_view(), name="cancel-order"),
    path('checkout/<int:pk>/', CheckoutAPIView.as_view(), name='checkout'),
    path('momo/webhook/', MomoWebhookAPIView.as_view(), name='momo_webhook'),
]