from django.shortcuts import render
from .models import Cart, CartItem
from store.views import _cart_id


def counter(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request=request))
                cart_items = CartItem.objects.filter(cart=cart)
            cart_count = sum([cart_item.quantity for cart_item in cart_items])
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
