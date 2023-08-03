from django.contrib import admin
from .models import Product, Variation, ReviewRating, Vendor


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('vendor',)


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_editable = ('is_active',)   # Cho phép chỉnh sửa trên list hiển thị
    list_filter = ('product', 'variation_category', 'variation_value')


class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'total_revenue', 'commission_rate', 'commission_price', 'status')
    list_editable = ('status',)
    list_filter = ('store_name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(Vendor, VendorAdmin)
