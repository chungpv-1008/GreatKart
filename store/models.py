from django.urls import reverse
from category.models import Category
from accounts.models import Account
from orders.models import OrderProduct
from django.db import models
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import six

mark_safe_lazy = lazy(mark_safe, six.text_type)
        

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
        "vendors.Vendor", related_name="products", on_delete=models.CASCADE)
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
