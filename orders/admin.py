from django.contrib import admin
from .models import (Order, 
                     OrderProduct, 
                     Payment, 
                     Shipping,
                     ShippingVendor,
                     )


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Shipping)
admin.site.register(ShippingVendor)