from django.urls import reverse
from category.models import Category
from accounts.models import Account
from orders.models import OrderProduct
from django.db import models
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from filer.fields.image import FilerImageField
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import date
import six

mark_safe_lazy = lazy(mark_safe, six.text_type)
        
COMMISSION_RATE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]



class Address(models.Model):
    address = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    district = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=50)
    class Meta:
        abstract = True


class ShopStatus(models.IntegerChoices):
    DISABLED = 0, _("disabled")
    ENABLED = 1, _("enabled")


# Create your models here.
class Vendor(Address):
    username = models.CharField(unique=True,blank=True,max_length=50)
    store_name = models.CharField(max_length=50,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("created on"))
    modified_on = models.DateTimeField(auto_now=True, editable=False, db_index=True, verbose_name=_("modified on"))
    domain = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("domain"),
        help_text=_(
            "Your shop domain name. Use this field to configure the URL that is used to visit your store front. "
            "Note: this requires additional configuration through your internet domain registrar."
        ),
    )
    status = models.IntegerField(
        choices=ShopStatus.choices,
        default=ShopStatus.DISABLED,
        verbose_name=_("status"),
        help_text=_(
            "Your shop's status. Disable your shop if it's no longer in use. "
            "For temporary closing enable the maintenance mode, available in the `Maintenance Mode` tab on the left."
        ),
    )
    prices_include_tax = models.BooleanField(
        default=True,
        verbose_name=_("prices include tax"),
        help_text=_(
            "This option defines whether product prices entered in admin include taxes. "
            "Note: this behavior can be overridden with contact group pricing."
        ),
    )
    commission_rate = models.FloatField(
        default=float(0),
        validators=COMMISSION_RATE_VALIDATOR
    )
    logo = FilerImageField(
        verbose_name=_("logo"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("Shop's logo. Will be shown at theme."),
        related_name="shop_logos",
    )

    favicon = FilerImageField(
        verbose_name=_("favicon"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_(
            "Shop's favicon - a mini-image graphically representing your shop. "
            "Depending on the browser, it will be shown next to the address bar "
            "and/or on the website title tab."
        ),
        related_name="shop_favicons",
    )

    def __str__(self):
        return self.store_name or ""

    @property
    def total_revenue(self):
        total_revenue = 0
        products = self.products.all()
        for product in products:
            order_item = OrderProduct.objects.get(product=product.id, vendor=self.id)
            if order_item.ordered:
                total_revenue += order_item.quantity * order_item.product_price 
        return total_revenue
    
    @property
    def commission_price(self):
        return self.commission_rate * self.total_revenue
    
    def commission_rate_in_percentage(self):
        return f"{self.commission_rate * 100} %"

    def save(self, *args, **kwargs):
        if not self.id:
            self.username = 'v' + str(date.today().year) +"-"+slugify(self.store_name)
            # ví dụ: 20% commission rate input nhập vào -> 0.2 trong database
            self.commission_rate = self.commission_rate / 100
        return super().save(*args, **kwargs)


class ShopProductVisibility(models.IntegerChoices):
    NOT_VISIBLE = 0, _("not visible")
    SEARCHABLE = 1
    LISTED = 2
    ALWAYS_VISIBLE = 3


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    # Khi xóa category thì Product bị xóa
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(
        Vendor, related_name="products", on_delete=models.CASCADE)
    # is_disabled = models.BooleanField(default=False)
    # disabled_start_time = models.DateTimeField()
    # disabled_duration = models.DurationField()
    visibility = models.IntegerField(
        default=ShopProductVisibility.ALWAYS_VISIBLE,
        choices=ShopProductVisibility.choices,
        db_index=True,
        verbose_name=_("visibility"),
        help_text=mark_safe_lazy(
            _(
                "Choose how you want your product to be seen and found by the customers. "
                "<p>Not visible: Product will not be shown in your store front nor found in search.</p>"
                "<p>Searchable: Product will be shown in search, but not listed on any category page.</p>"
                "<p>Listed: Product will be shown on category pages, but not shown in search results.</p>"
                "<p>Always Visible: Product will be shown in your store front and found in search.</p>"
            )
        ),
    )

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
