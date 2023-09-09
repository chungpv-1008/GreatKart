from django_tables2 import Table
from store.models import Product
from orders.models import Order

class ProductTable(Table):
    class Meta:
        model = Product
        template_name = "includes/table.html"


class OrderTable(Table):
    class Meta:
        model = Order
        template_name = "includes/table.html"