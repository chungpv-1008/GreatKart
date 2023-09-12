from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from accounts.models import Account


class Payment(models.Model):
    PAYPAL = 'P'
    MOMO = 'M'
    COD = 'C'

    PAYMENT_CHOICES = ((PAYPAL, _('paypal')), (MOMO, _('momo')), (COD, _('cod')))

    STATUS_CHOICES = (("PENDING", _('pending')), ("COMPLETED",
                    _('completed')), ("FAILED", _('failed')))
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default="M")
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    

class ShippingVendor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    estimated_delivery_time = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
     

class Shipping(models.Model):
    price = models.IntegerField()
    shipping_method = models.ForeignKey(ShippingVendor, on_delete=models.CASCADE)
    tracking_number = models.CharField(blank=True, max_length=20)
    tracking_url = models.CharField(blank=True, max_length=100)


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    shipping = models.OneToOneField(Shipping, on_delete=models.SET_NULL, null=True, related_name="order")
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, blank=True, null=True, related_name="order")
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, null=True)
    shipping_address = models.CharField(max_length=100)

    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def full_address(self):
        return "{0} {1}".format(self.address_line_1, self.address_line_2)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    variations = models.ManyToManyField('store.Variation', blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

    @cached_property
    def cost(self):
        """
        Total cost of the ordered item
        """
        return round(self.quantity * self.product.price, 2)