from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from accounts.models import CustomUser, Profile
from .utils import send_verification_email


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import CustomUser


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        if not phone or not password:
            raise serializers.ValidationError("شماره موبایل و رمز عبور لازم است.")

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("کاربری با این شماره موبایل یافت نشد.")

        if not user.check_password(password):
            raise serializers.ValidationError("رمز عبور اشتباه است.")

        if not user.is_verified:
            raise serializers.ValidationError("ایمیل شما هنوز تأیید نشده است.")

        # ایجاد توکن‌ها (مستقیم، بدون super)
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "phone": user.phone,
            "full_name": user.full_name,
            "role": user.role,
            "email": user.email,
            "is_verified": user.is_verified,
        }

        return data

# ✅ تغییر رمز عبور
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


# ✅ ثبت‌نام کاربر جدید
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=5)
    password2 = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = CustomUser
        fields = ['phone', 'full_name', 'email', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("رمزها با یکدیگر مطابقت ندارند.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        user = CustomUser.objects.create_user(password=password, **validated_data)
        user.is_verified = False

        request = self.context.get('request')
        send_verification_email(request, user)

        user.save()
        return user


# ✅ مشاهده و ویرایش پروفایل
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_id', 'birth_date', 'address', 'profile_picture']
        read_only_fields = ['user', 'updated_date']
