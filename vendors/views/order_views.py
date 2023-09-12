from django.shortcuts import render
from vendors.decorators import vendor_required
from vendors.models import Vendor
from orders.models import Order
from vendors.tables import OrderTable

@vendor_required
def list_order_view(request):
    vendor = Vendor.objects.get(user=request.user)
    completed_orders = Order._default_manager.filter(
        # status="Completed",
        vendor=vendor.id
    )
    table = OrderTable(completed_orders)
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, 'vendor/list_order.html', {
        'order_table': table,
        'orders': completed_orders
    })