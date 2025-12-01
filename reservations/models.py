from django.db import models
from django.utils import timezone
from seat.models import Seat
from accounts.models import Profile


class Reservation(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'در انتظار پرداخت'
        PAID = 'PAID', 'پرداخت شده'
        FAILED = 'FAILED', 'پرداخت ناموفق'
        REFUNDED = 'REFUNDED', 'برگشت داده شده'

    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reservation_code = models.CharField(max_length=20, unique=True, verbose_name="کد رزرو")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="مبلغ کل")
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="وضعیت پرداخت",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            import random
            import string

            self.reservation_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        if not self.total_price and self.seat_id:
            self.total_price = self.seat.trip.current_price
        super().save(*args, **kwargs)

    def mark_as_paid(self):
        self.payment_status = self.PaymentStatus.PAID
        self.save(update_fields=['payment_status', 'updated_at'])

    def mark_as_failed(self):
        self.payment_status = self.PaymentStatus.FAILED
        self.save(update_fields=['payment_status', 'updated_at'])
        self.release_seat()

    def mark_as_refunded(self):
        self.payment_status = self.PaymentStatus.REFUNDED
        self.save(update_fields=['payment_status', 'updated_at'])
        self.release_seat()

    def reserve_seat(self):
        seat = self.seat
        if seat.is_reserved and seat.reserved_by_id != self.user_id:
            raise ValueError("Seat already reserved.")
        seat.is_reserved = True
        seat.reserved_by = self.user
        seat.reserved_at = timezone.now()
        seat.save(update_fields=['is_reserved', 'reserved_by', 'reserved_at'])

    def release_seat(self):
        seat = self.seat
        if not seat.is_reserved:
            return
        seat.is_reserved = False
        seat.reserved_by = None
        seat.reserved_at = None
        seat.save(update_fields=['is_reserved', 'reserved_by', 'reserved_at'])

    @property
    def passenger_info(self):
        profile = self.user
        return {
            'name': f"{profile.first_name} {profile.last_name}",
            'phone': profile.user.phone,
            'national_id': profile.national_id,
            'full_name': profile.user.full_name,
        }

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