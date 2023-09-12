from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from store.models import Product
from django.contrib.auth.forms import AuthenticationForm

from .models import Vendor


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ('product_name', 'category', 'price', 'description',
                  'images', 'is_available')
        labels = {
            'product_name': 'Product name',
            'category': 'Category',
            'price': 'Price',
            'description': 'Description',
            'size': 'Size',
            'images': 'Image',
            'is_available': 'Available',
        }


class VendorAuthenticationForm(AuthenticationForm):
    
    def confirm_login_allowed(self, user):
        DISABLE = 0
        vendor = Vendor.objects.filter(user=user).first()
        if not user.is_admin:
            raise forms.ValidationError('The user is not admin', code='invalid_login')
        if vendor.status == DISABLE:
            raise forms.ValidationError('The vendor has been disabled', code='invalid_login')