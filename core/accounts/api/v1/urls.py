from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    CustomTokenObtainPairView,
    ChangePasswordView,
    ProfileView,
    RegisterView,
    LogoutView,
    VerifyEmailView,
    test_reverse
)

urlpatterns = [
    # 🔐 Login - دریافت توکن JWT
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),

    # 🔄 Refresh token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ بررسی اعتبار توکن
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # 🔐 ثبت‌نام کاربر جدید
    path('auth/register/', RegisterView.as_view(), name='register'),

    # 🔐 تغییر رمز عبور (فقط برای کاربر احراز هویت شده)
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),

    # 🔐 خروج (در حال حاضر فقط پیام می‌ده)
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # 👤 پروفایل کاربر
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # ✅ تأیید ایمیل
    path('auth/verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='email-verify'),

    # ⚙️ فقط برای تست reverse
    # path('auth/test/', test_reverse)
]
