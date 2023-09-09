from django.shortcuts import render, get_object_or_404
from vendors.models import Vendor

def storefront(request, vendor_name):
    ENABLED = 1
    vendor = get_object_or_404(Vendor, store_name=vendor_name, status=ENABLED)
    products = vendor.products.all()
    request.session['vendor'] = vendor
    context = {
        'products': products,
    }
    return render(request, 'home.html', context=context)
