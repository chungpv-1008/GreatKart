from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsSellerOrAdmin(BaseException):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user or request.user.is_admin
    

class IsPaymentByUser(BaseException):
    """
    Check if payment belongs to the appropriate buyer or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.order.buyer == request.user or request.user.is_staff


class IsPaymentPending(BasePermission):
    """
    Check if the status of payment is pending or completed before updating/deleting instance
    """
    message = _('Updating or deleting completed payment is not allowed.')

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve',):
            return True
        return obj.status == 'PENDING'
    

class IsOrderPendingWhenCheckout(BasePermission):
    """
    Check the status of order is pending or completed before updating instance
    """
    message = _('Updating closed order is not allowed.')

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET',):
            return True
        return obj.status == 'New'