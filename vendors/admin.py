from django.contrib import admin
from .models import Vendor

from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Case, When, Q, DecimalField
from datetime import date, timedelta, datetime


class OrderDateFilter(admin.SimpleListFilter):
    title = _('Order Date')
    parameter_name = 'order_date_is_ordered'

    def lookups(self, request, model_admin):
        return [
            ('today_ordered', _('Today (Ordered)')),
            ('last_7_days_ordered', _('Last 7 Days (Ordered)')),
            ('last_30_days_ordered', _('Last 30 Days (Ordered)')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'today_ordered':
            today = datetime.today()
            return queryset.filter(order__created_at__date=today, order__is_ordered=True)
        elif self.value() == 'last_7_days_ordered':
            seven_days_ago = datetime.now() - timedelta(days=7)
            return queryset.annotate(
                order_total_filtered=Sum(
                    Case(
                        When(order__created_at__gte=seven_days_ago, order__is_ordered=True, then='order__order_total'),
                        default=0,
                        output_field=DecimalField()
                    )
                )
            )
        elif self.value() == 'last_30_days_ordered':
            thirty_days_ago = datetime.now() - timedelta(days=30)
            return queryset.annotate(
                order_total_filtered=Sum(
                    Case(
                        When(order__created_at__gte=thirty_days_ago, order__is_ordered=True, then='order__order_total'),
                        default=0,
                        output_field=DecimalField()
                    )
                )
            )


class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'revenue', 'commission_rate_in_percentage', 'commission_price', 'status')
    list_editable = ('status',)
    list_filter = ('store_name', OrderDateFilter,)

    def revenue(self, obj):
        return f"${obj.order_total_filtered:.2f}" if hasattr(obj, 'order_total_filtered') and obj.order_total_filtered is not None else "$0.00"
    revenue.short_description = 'Revenue'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(order_total_filtered=Sum('order__order_total', filter=Q(order__is_ordered=True)))

admin.site.register(Vendor, VendorAdmin)