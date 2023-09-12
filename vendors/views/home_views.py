# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import redirect, render
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from orders.models import Order
from vendors.models import Vendor
from store.models import Product
User = get_user_model()

@login_required(login_url="/vendor/sign-in")
def home(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order._default_manager.filter(
        status="Completed",
        vendor=vendor.id
    )
    buyers = User._default_manager.filter(
        order__vendor=vendor.id
    ).distinct()
    products = Product._default_manager.filter(
        vendors__in=[vendor.id]
    ).distinct()
    total_users = buyers.count()
    total_revenue = vendor.total_revenue
    total_products = products.count()
    context = {
        "total_orders": orders.count(),
        "total_users": total_users,
        "total_revenue": total_revenue,
        "total_products": total_products
    }
    return render(request, 'home/index.html', context)
