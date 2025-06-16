from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile , CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs,):
        data = super().validate(attrs)

        data["phone"] = self.user.phone
        data["full-name"] = self.user.full_name
        data["role"] = self.user.role
        data["email"] = self.user.email
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = CustomUser
        fields = ['phone', 'full_name', 'password', 'email']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_id', 'birth_date', 'address', 'profile_picture']
        read_only_fields = ['user', 'updated_date']

