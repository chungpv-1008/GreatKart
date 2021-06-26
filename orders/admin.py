from django.contrib import admin
from .models import Order, OrderProduct, Payment


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct)
