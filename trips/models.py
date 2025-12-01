from django.db import models
from django.core.exceptions import ValidationError
from fleet.models import Fleet
from routes.models import Route

class Trip(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'برنامه‌ریزی شده'),
        ('BOARDING', 'در حال سوار شدن'),
        ('DEPARTED', 'حرکت کرده'),
        ('ARRIVED', 'رسیده'),
        ('CANCELLED', 'لغو شده'),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="مسیر")
    bus = models.ForeignKey(Fleet, on_delete=models.CASCADE, verbose_name="اتوبوس")
    departure_datetime = models.DateTimeField(verbose_name="زمان حرکت")
    arrival_datetime = models.DateTimeField(verbose_name="زمان رسیدن")
    current_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت فعلی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                            default='SCHEDULED', verbose_name="وضعیت")
    # driver_phone = models.CharField(max_length=15, verbose_name="تلفن راننده")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سفر"
        verbose_name_plural = "سفرها"
        ordering = ['-departure_datetime']
        indexes = [
            models.Index(fields=['departure_datetime', 'status']),
            models.Index(fields=['route', 'departure_datetime']),
        ]

    def clean(self):
        # if self.departure_datetime <= timezone.now():
        #     raise ValidationError("زمان حرکت باید در آینده باشد")
        
        if self.arrival_datetime <= self.departure_datetime:
            raise ValidationError("زمان رسیدن باید بعد از زمان حرکت باشد")
        
        if self.bus.company != self.route.company:
            raise ValidationError("اتوبوس باید متعلق به همان شرکت مسیر باشد")
        
        if self.bus.bus_type != self.route.bus_type:
            raise ValidationError("نوع اتوبوس باید با نوع تعریف شده در مسیر یکسان باشد")

    # def save(self, *args, **kwargs):
    #     # تنظیم قیمت فعلی بر اساس قیمت مسیر (اگر تعیین نشده)
    #     if not self.current_price:
    #         self.current_price = self.route.base_price
        
    #     super().save(*args, **kwargs)
        
    #     # ساخت خودکار صندلی‌ها بعد از ذخیره سفر
    #     self.create_seats()

    # def create_seats(self):
    #     """ساخت خودکار صندلی‌ها برای این سفر"""
    #     from seats.models import Seat
        
    #     # اگر صندلی وجود ندارد، بساز
    #     if not self.seats.exists():
    #         seats_to_create = []
    #         for seat_num in range(1, self.bus.capacity + 1):
    #             seats_to_create.append(
    #                 Seat(trip=self, seat_number=seat_num)
    #             )
    #         Seat.objects.bulk_create(seats_to_create)

    def __str__(self):
        return f"{self.route.route_name} | {self.departure_datetime.strftime('%Y-%m-%d %H:%M')}"

    # @property
    # def available_seats_count(self):
    #     return self.seats.filter(is_reserved=False).count()

    # @property
    # def is_full(self):
    #     return self.available_seats_count == 0