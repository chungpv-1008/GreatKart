from django.urls import path, include
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('momo_payment/', views.momo_payment, name='momo_payment'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
