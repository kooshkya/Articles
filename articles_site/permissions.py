from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta


class IsAuthenticatedAndRegisteredOver10Days(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        account_age = timezone.now() - request.user.date_joined
        return account_age >= timedelta(days=10)
