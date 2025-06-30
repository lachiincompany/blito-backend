from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth.models import User

from accounts.models import CustomUser
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    ProfileSerializer
)


# ✅ لاگین با JWT همراه با بررسی تأیید ایمیل
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ✅ ثبت‌نام کاربر جدید
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


# ✅ تغییر رمز عبور
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": "رمز فعلی اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data.get("new_password"))
            user.save()

            return Response({"detail": "رمز عبور با موفقیت تغییر یافت. لطفاً دوباره وارد شوید."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ خروج کاربر (بدون بلاک‌لیست کردن توکن)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"detail": "با موفقیت خارج شدید."}, status=status.HTTP_200_OK)


# ✅ مشاهده و ویرایش پروفایل کاربر
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# ✅ تأیید ایمیل کاربر از طریق لینک
class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception:
            return Response({'detail': 'لینک نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            return Response({'detail': '✅ ایمیل با موفقیت تأیید شد.'})
        return Response({'detail': '❌ لینک منقضی یا نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)


# ✅ فقط برای تست معکوس کردن URL
def test_reverse(request):
    url = reverse('accounts:email-verify', kwargs={'uidb64': 'abc', 'token': '123'})
    return HttpResponse(f"url: {url}")
