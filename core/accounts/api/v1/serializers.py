from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from accounts.models import CustomUser, Profile
from .utils import send_verification_email


# ✅ لاگین همراه با بررسی تایید ایمیل
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError("ایمیل شما هنوز تأیید نشده است.")

        data.update({
            "phone": self.user.phone,
            "full_name": self.user.full_name,
            "role": self.user.role,
            "email": self.user.email,
            "is_verified": self.user.is_verified
        })

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
