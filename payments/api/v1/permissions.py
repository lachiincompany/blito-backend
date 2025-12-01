from rest_framework import permissions


class IsPaymentOwnerOrAdmin(permissions.BasePermission):
    """
    اجازه دسترسی فقط برای صاحب رزرو یا ادمین
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.reservation.user.user == request.user

