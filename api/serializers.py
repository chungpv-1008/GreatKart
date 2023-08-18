from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from category.models import Category
from store.models import Product, ReviewRating, Variation
from orders.models import Order, OrderProduct, Shipping, Payment
from vendors.models import Vendor


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model: Variation
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'


class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'quantity',
                  'product_price', 'cost', 'created_at', 'updated_at', )
        read_only_fields = ('order', )

    def validate(self, validated_data):
        order_quantity = validated_data['quantity']
        product_quantity = validated_data['product'].quantity

        order_id = self.context['view'].kwargs.get('order_id')
        product = validated_data['product']
        current_item = OrderProduct.objects.filter(
            order__id=order_id, product=product)

        if(order_quantity > product_quantity):
            error = {'quantity': _('Ordered quantity is more than the stock.')}
            raise serializers.ValidationError(error)

        if not self.instance and current_item.count() > 0:
            error = {'product': _('Product already exists in your order.')}
            raise serializers.ValidationError(error)

        if self.context['request'].user == product.seller:
            error = _('Adding your own product to your order is not allowed')
            raise PermissionDenied(error)

        return validated_data

    def get_cost(self, obj):
        return obj.quantity * obj.product.price


class OrderReadSerializer(serializers.ModelSerializer):
    order_items = OrderProductSerializer(read_only=True, many=True)
    vendor_info = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), source='vendor')

    class Meta:
        model = Order
        fields = ('id', 'user', 'shipping_address', 'shipping', 'payment', 'address_line_1', 'address_line_2', 'country',
                  'order_items', 'order_total', 'status', 'created_at', 'updated_at', 'vendor_info')


class OrderWriteSerializer(serializers.ModelSerializer):

    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'buyer', 'status', 'order_items', 'address_line_1', 'address_line_2', 'country',
                  'shipping_address', 'created_at', 'updated_at', 'vendor')
        read_only_fields = ('status', )

    def create(self, validated_data):
        orders_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for order_data in orders_data:
            OrderProduct.objects.create(order=order, **order_data)

        return order

    def update(self, instance, validated_data):
        orders_data = validated_data.pop('order_items', None)
        orders = list((instance.order_items).all())

        if orders_data:
            for order_data in orders_data:
                order = orders.pop(0)
                order.product = order_data.get('product', order.product)
                order.quantity = order_data.get('quantity', order.quantity)
                order.save()

        return instance


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_id', )
