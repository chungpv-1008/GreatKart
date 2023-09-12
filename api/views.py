from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from category.models import Category
from .permissions import (
    IsSellerOrAdmin,
    IsPaymentPending,
    IsOrderPendingWhenCheckout
    )
from store.models import Product
from orders.models import Order, Shipping, Payment
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    OrderWriteSerializer,
    OrderReadSerializer,
    ShippingSerializer,
    CheckoutSerializer,
    PaymentSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ('create', ):
            self.permission_classes = (permissions.AllowAny, )#permissions.IsAuthenticated, )
        elif self.action in ('update', 'partial_update', 'destroy', ):
            self.permission_classes = (permissions.AllowAny, )
        else:
            self.permission_classes = (permissions.AllowAny, )
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return OrderWriteSerializer

        return OrderReadSerializer



class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(order__buyer=user.id)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsPaymentPending]

        return super().get_permissions()


class OrderCancelAPIView(APIView):
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        order.status = 'Cancelled'
        order.save()
        return Response(status=status.HTTP_200_OK)


class CheckoutAPIView(UpdateAPIView):
    """
    Create, Retrieve, Update billing address, shipping address and payment of an order
    """
    queryset = Order.objects.all()
    serializer_class = CheckoutSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            self.permission_classes += [IsOrderPendingWhenCheckout]

        return super().get_permissions()
    

class MomoWebhookAPIView(APIView):
    """
    Stripe webhook API view to handle checkout session completed and other events.
    """

    def post(self, request, format=None):
        status_code = request.POST.get('statusCode')
        order_number = request.POST.get('orderId')
        if status_code == 0:
            order = get_object_or_404(Order, order_number=order_number)
            order.status = 'Completed'
            order.save()

            payment = get_object_or_404(Payment, order_payment=order.id)
            payment.status = 'COMPLETED'
            payment.save()

        return Response(status=status.HTTP_200_OK)
    

# class VnpayWebhookAPIView(APIView):
#     def post(self, request):
#         vnp = vnpay()
#         vnp.requestData['vnp_Version'] = '2.0.0'
#         vnp.requestData['vnp_Command'] = 'pay'
#         vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
#         vnp.requestData['vnp_Amount'] = amount * 100
#         vnp.requestData['vnp_CurrCode'] = 'VND'
#         vnp.requestData['vnp_TxnRef'] = orderId
#         vnp.requestData['vnp_OrderInfo'] = order_desc
#         vnp.requestData['vnp_OrderType'] = order_type
#         # Check language, default: vn
#         if language and language != '':
#             vnp.requestData['vnp_Locale'] = language
#         else:
#             vnp.requestData['vnp_Locale'] = 'vn'
#             # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
#         if bank_code and bank_code != "":
#             vnp.requestData['vnp_BankCode'] = bank_code

#         vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
#         vnp.requestData['vnp_IpAddr'] = ipaddr
#         vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
#         vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
#         print(vnpay_payment_url)
#         if request.is_ajax():
#             # Show VNPAY Popup
#             result = JsonResponse({'code': '00', 'Message': 'Init Success', 'data': vnpay_payment_url})
#             return result


class OrderPayAPIView(APIView):
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        payload = self.request.body 
        if self.request.method == 'POST':
            
            order = get_object_or_404(Order, order_number=payload['order_number'])
            order.status = 'Completed'
            order.save()

            payment = get_object_or_404(Payment, order_payment=order.id)
            payment.status = 'COMPLETED'
            payment.save()
            return Response( status=status.HTTP_200_OK)