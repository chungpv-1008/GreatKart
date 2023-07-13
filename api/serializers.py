from rest_framework import serializers

from category.models import Category
from store.models import Product, ReviewRating, Variation


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model: Variation
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.HiddenField(
        default=serializers.CurrentUserDefault() 
    )
    
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