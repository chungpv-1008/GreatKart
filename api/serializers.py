from rest_framework import serializers

from category.models import Category
from store.models import Product, ReviewRating, Variation
from orders.models import Order


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


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
