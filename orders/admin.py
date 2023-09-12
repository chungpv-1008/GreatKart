from django.contrib import admin
from .models import (Order, 
                     OrderProduct, 
                     Payment, 
                     Shipping,
                     ShippingVendor,
                     )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'status', 'vendor')

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Shipping)
admin.site.register(ShippingVendor)