# permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    مجوز سفارشی: فقط صاحب رزرو یا ادمین می‌تواند دسترسی داشته باشد
    """
    
    def has_object_permission(self, request, view, obj):
        # ادمین‌ها دسترسی کامل دارند
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # کاربران فقط به رزروهای خودشان دسترسی دارند
        return obj.user.user == request.user
