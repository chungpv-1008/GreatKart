from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from .views import home_views, product_views, sign_in_views, sign_out_views, storefront_views

app_name = 'vendor'

urlpatterns = [
    # root_path
        # The home page
    # path('', home_views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', home_views.pages, name='pages'),
    path('', home_views.home, name='root_path'),
    # auth_path
    # path('sell-on-lomofy', sign_up_views.VendorSignUpView, name='vendor_sign_up'),
    path('sign-in', sign_in_views.SignInView.as_view(), name='vendor_sign_in'),
    path(
        "sign-out",
        sign_out_views.SignOutView.as_view(),
        name="vendor_sign_out",
    ),

    # Product management urls
    path('add-product', product_views.create_product_view, name='add_product'),
    path('edit/<int:product_id>', product_views.edit_product_view, name='edit_product'),
    path('<str:vendor_name>', storefront_views.storefront, name='storefront' )
]
