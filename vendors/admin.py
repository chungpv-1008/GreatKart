from django.contrib import admin
from .models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'total_revenue', 'commission_rate', 'commission_price', 'status')
    list_editable = ('status',)
    list_filter = ('store_name',)

admin.site.register(Vendor, VendorAdmin)