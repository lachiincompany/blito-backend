from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
import re 
from django.utils.translation import gettext_lazy as _ 
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class CustomUserManager(BaseUserManager):

    def _validate_phone(self, phone):
        """
        validate phone number
        """
        if not phone:
            raise ValidationError("شماره تلفن الزامی هستش")
        phone = re.sub(r'\D', '', phone)
        if not re.match(r'^09\d{9}$', phone):
            raise ValidationError("شماره تلفن باید 11 رقمی باشد و با 09 شروع شود")
        return phone 
    
    def create_user(self, phone, password=None, **extra_fields):
        phone = self._validate_phone(phone)
        email = extra_fields.get('email')
        if email:
            extra_fields['email'] = self.normalize_email(email)
        
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        create and save a superuser with the given phone number and password
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValidationError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValidationError(_("Superuser must have is_superuser=True."))
        # if not extra_fields.get("is_verified"):
        #     raise ValidationError(_("Superuser must have is_verified=True."))
        
        return self.create_user(phone, password, **extra_fields)
    
    def get_by_natural_key(self, phone):
        """
        Retrieve a user by their phone number
        """
        phone = self._validate_phone(phone)
        return self.get(phone=phone)
        


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'مسافر'),
        ('driver', 'راننده'),
        ('admin', 'مدیر'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer',
        verbose_name='نقش کاربر'
    )
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    full_name = models.CharField(max_length=100, verbose_name="نام کامل")
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name="ایمیل")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت")
    is_staff = models.BooleanField(default=False, verbose_name="کارمند")
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت نام")


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone}({self.full_name})"
    

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

class Profile(models.Model):
    """
    Profile model to store additional user information.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile", verbose_name="کاربر")
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    national_id = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name='کد ملی',
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    address = models.TextField(null=True, blank=True, verbose_name="آدرس")
    updated_date = models.DateTimeField(auto_now=True, verbose_name='آخرین برزورسانی')
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, verbose_name="عکس پروفایل")


        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
        
    
@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update a profile when a CustomUser is created or updated.
    """
    if created:
        Profile.objects.create(user=instance)
    