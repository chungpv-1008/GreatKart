from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'products', ProductViewSet, basename="product")
router.register(r'orders', OrderViewSet, basename="order")

urlpatterns = [
    path('', include(router.urls)),
]