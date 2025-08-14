from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from trips.models import Trip
from accounts.models import Profile

User = get_user_model()

class Seat(models.Model):
    trip = models.ForeignKey(Trip, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField(verbose_name="شماره صندلی")
    is_reserved = models.BooleanField(default=False, verbose_name="رزرو شده")
    reserved_by = models.ForeignKey(Profile, null=True, blank=True, 
                                  on_delete=models.SET_NULL, verbose_name="رزرو شده توسط")
    reserved_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان رزرو")

    class Meta:
        verbose_name = "صندلی"
        verbose_name_plural = "صندلی‌ها"
        unique_together = ('trip', 'seat_number')
        ordering = ['seat_number']
        indexes = [
            models.Index(fields=['trip', 'is_reserved']),
        ]

    def clean(self):
        if self.seat_number > self.trip.bus.capacity:
            raise ValidationError(f"شماره صندلی نباید بیشتر از ظرفیت اتوبوس ({self.trip.bus.capacity}) باشد")

    def reserve(self, user):
        """رزرو صندلی با استفاده از اطلاعات Profile کاربر"""
        if self.is_reserved:
            raise ValidationError("این صندلی قبلاً رزرو شده است")
        
        if self.trip.departure_datetime <= timezone.now():
            raise ValidationError("نمی‌توان برای سفرهای گذشته رزرو انجام داد")
        
        if not hasattr(user, 'profile') or not user.profile.national_id:
            raise ValidationError("لطفاً ابتدا پروفایل خود را تکمیل کنید")
        
        self.is_reserved = True
        self.reserved_by = Profile.objects.get(user=user)
        self.reserved_at = timezone.now()
        self.save()

    def cancel_reservation(self):
        """لغو رزرو"""
        if not self.trip.can_cancel:
            raise ValidationError("زمان لغو رزرو گذشته است")
        
        self.is_reserved = False
        self.reserved_by = None
        self.reserved_at = None
        self.save()

    @property
    def passenger_info(self):
        """دریافت اطلاعات مسافر از Profile"""
        if self.reserved_by and hasattr(self.reserved_by, 'profile'):
            profile = self.reserved_by.profile
            return {
                'name': f"{profile.first_name} {profile.last_name}",
                'phone': self.reserved_by.phone,
                'national_id': profile.national_id,
            }
        return None
    

    def __str__(self):
        status = "رزرو شده" if self.is_reserved else "آزاد"
        return f"سفر {self.trip.id} - صندلی {self.seat_number} ({status})"