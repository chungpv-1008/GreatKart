from rest_framework import viewsets, permissions

from category.models import Category
from .permissions import IsSellerOrAdmin
from store.models import Product
from orders.models import Order, Shipping, Payment
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    OrderWriteSerializer,
    OrderReadSerializer,
    ShippingSerializer,
    PaymentSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ('create', ):
            self.permission_classes = (permissions.AllowAny, )#permissions.IsAuthenticated, )
        elif self.action in ('update', 'partial_update', 'destroy', ):
            self.permission_classes = (permissions.AllowAny, )
        else:
            self.permission_classes = (permissions.AllowAny, )
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer



class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
