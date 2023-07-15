from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsSellerOrAdmin(BaseException):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user or request.user.is_admin