from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile , CustomUser
from .utils import send_verification_email
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs,):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError("ایمیل شما هنوز تایید نشده است")
        data["phone"] = self.user.phone
        data["full-name"] = self.user.full_name
        data["role"] = self.user.role
        data["email"] = self.user.email
        data["is_verified"] = self.user.is_verified
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=5)
    password2 = serializers.CharField(write_only=True, min_length=5)
    class Meta:
        model = CustomUser
        fields = ['phone', 'full_name', 'password1','password2', 'email']
    

    def validate(self, data):
        if data['password1'] != data["password2"]:
            raise serializers.ValidationError("رمز های مطابقت ندارند")
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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_id', 'birth_date', 'address', 'profile_picture']
        read_only_fields = ['user', 'updated_date']

