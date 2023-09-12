from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    CategoryViewSet,
    ProductViewSet, 
    OrderViewSet, 
    PaymentViewSet, 
    ShippingViewSet, 
    OrderPayAPIView,
    OrderCancelAPIView,
    CheckoutAPIView,
    MomoWebhookAPIView
)

schema_view = get_schema_view(
    openapi.Info(title="NineHealth API", default_version='v1'),
    public=True,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'products', ProductViewSet, basename="product")
router.register(r'orders', OrderViewSet, basename="order")
# router.register(r'payments', PaymentViewSet, basename="payment")
router.register(r'shipping', ShippingViewSet, basename="shipping")
urlpatterns = [
    path('', include(router.urls)),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'orders/cancel-order/<int:order_id>', OrderCancelAPIView.as_view(), name="cancel-order"),
    path(r'orders/pay', OrderPayAPIView.as_view(), name="pay-order"),
    path('checkout/<int:pk>/', CheckoutAPIView.as_view(), name='checkout'),
    path('momo/webhook/', MomoWebhookAPIView.as_view(), name='momo_webhook'),
]