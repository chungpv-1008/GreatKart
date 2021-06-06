from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect

from store.models import Product, Variation
from carts.models import Cart, CartItem


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)    # Get object product
    product_variations = list()
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variations.append(variation)
            except ObjectDoesNotExist:
                pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    is_exists_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_exists_cart_item:
        cart_items = CartItem.objects.filter(
            product=product,
            cart=cart
        )
        existing_variation_list = [list(item.variations.all()) for item in cart_items]
        id = [item.id for item in cart_items]
        if product_variations in existing_variation_list:
            idex = existing_variation_list.index(product_variations)
            cart_item = CartItem.objects.get(id=id[idex])
            cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
    if len(product_variations) > 0:
        cart_item.variations.clear()
        for item in product_variations:
            cart_item.variations.add(item)
    cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            product=product,
            cart=cart
        )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request=request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            id=cart_item_id,
            product=product,
            cart=cart
        )
        cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = total * 2 / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context=context)
