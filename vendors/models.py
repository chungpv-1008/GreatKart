from django.db import models
from django.utils.text import slugify
from filer.fields.image import FilerImageField
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import date
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import six

from orders.models import Order

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
    user = models.OneToOneField(
        "accounts.Account", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(blank=True,max_length=50)
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
        orders = Order.objects.filter(vendor=self.id)
        if len(orders):
            total_revenue = sum([
                order.order_total 
                for order in orders
                if order.is_ordered
            ])
        return total_revenue
    
    @property
    def commission_price(self):
        return (self.commission_rate * self.total_revenue) / 100
    
    def commission_rate_in_percentage(self):
        return f"{self.commission_rate} %"

    def save(self, *args, **kwargs):
        if not self.id:
            self.username = 'v' + str(date.today().year) +"-"+slugify(self.store_name)
        return super().save(*args, **kwargs)
