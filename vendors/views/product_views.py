from django.contrib.auth import login
from django.shortcuts import redirect, render
from vendors.decorators import vendor_required
from vendors.forms import ProductForm
from vendors.models import Vendor
from orders.models import Order
from store.models import Product
from vendors.tables import ProductTable

@vendor_required
def create_product_view(request):
    """Add a product to the vendor's product list."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = Vendor.objects.get(user=request.user)
            product.save()
            return redirect('vendor:vendor_root')
    else:
        form = ProductForm()
    return render(request, 'vendor/add_product_form.html', {'form': form})


@vendor_required
def edit_product_view(request, product_id):
    """Edit a product in the vendor's product list."""
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = Vendor.objects.get(user=request.user)
            product.save()
            return redirect('vendor:vendor_root')
    else:
        form = ProductForm(instance=product)
    return render(request, 'vendor/edit_product_form.html', {'form': form})

@vendor_required
def list_product_view(request):
    vendor = Vendor.objects.get(user=request.user)
    products = Product._default_manager.filter(
        vendors__in=[vendor.id]
    ).distinct()
    completed_orders = Order._default_manager.filter(
        status="Completed",
        vendor=vendor.id
    )
    product_revenue = {}
    for order in completed_orders:
        order_items = order.orderitem_set.all()
        for item in order_items:
            product = item.product
            quantity = item.quantity
            price = product.price  # Assuming your Product model has a 'price' field
            revenue = quantity * price

            # Update the product revenue in the dictionary
            if product.id in product_revenue:
                product_revenue[product.id] += revenue
            else:
                product_revenue[product.id] = revenue

    table = ProductTable(products)
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, 'vendor/list_product.html', {
        'table': table,
        'products': products
    })

def table(request):
    return render(request, 'home/tables.html')