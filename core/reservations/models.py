from django.db import models
from seat.models import Seat
from django.contrib.auth import get_user_model
from accounts.models import Profile
# Create your models here.

User = get_user_model()

class Reservation(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reservation_code = models.CharField(max_length=20, unique=True, verbose_name="کد رزرو")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="مبلغ کل")
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'در انتظار پرداخت'),
        ('PAID', 'پرداخت شده'),
        ('FAILED', 'پرداخت ناموفق'),
        ('REFUNDED', 'برگشت داده شده'),
    ], default='PENDING', verbose_name="وضعیت پرداخت")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.reservation_code:
            import random, string
            self.reservation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    @property
    def passenger_info(self):
        if hasattr(self.user, 'profile'):
            profile = self.user
            return {
                'name': f"{profile.first_name} {profile.last_name}",
                'phone': self.user.user.phone,
                'national_id': profile.national_id,
                'full_name': self.user.user.full_name,
            }
        return {'phone': self.user.user.phone, 'full_name': self.user.user.full_name}

    @property
    def trip_info(self):
        return {
            'origin': self.seat.trip.route.origin.city.name,
            'destination': self.seat.trip.route.destination.city.name,
            'departure_datetime': self.seat.trip.departure_datetime,
            'company': self.seat.trip.route.company.name,
            'bus_type': self.seat.trip.bus.bus_type,
            'seat_number': self.seat.seat_number,
        }

    def __str__(self):
        return f"رزرو {self.reservation_code} - {self.user.user.phone}"

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزروها"
        ordering = ['-created_at']