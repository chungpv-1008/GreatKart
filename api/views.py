from rest_framework import viewsets, permissions

from category.models import Category
from .permissions import IsSellerOrAdmin
from store.models import Product
from orders.models import Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer


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
            self.permission_classes = (IsSellerOrAdmin, )
        else:
            self.permission_classes = (permissions.AllowAny, )
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
