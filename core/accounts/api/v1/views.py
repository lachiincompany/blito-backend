from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    ChangePasswordSerializer, 
    MyTokenObtainPairSerializer,
    ProfileSerializer,
    RegisterSerializer,
    )
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from accounts.models import CustomUser
from rest_framework.views import APIView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # بررسی رمز فعلی
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": "رمز فعلی اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

            # تنظیم رمز جدید
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()


            return Response({"detail": "رمز با موفقیت تغییر کرد. لطفاً دوباره وارد شوید."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"detail": "با موفقیت خارج شدید."}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    

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
        else:
            return Response({'detail': '❌ لینک منقضی یا نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

from django.urls import reverse
from django.http import HttpResponse
       
def test_reverse(request):
    url = reverse('email-verify', kwargs={'uidb64': 'abc', 'token': '123'})
    return HttpResponse(f"url: {url}")