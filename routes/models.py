from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from city.models import Terminal
from bus_companies.models import BusCompany

class Route(models.Model):
    origin = models.ForeignKey(Terminal, related_name='routes_from', 
                             on_delete=models.CASCADE, verbose_name="مبدا")
    destination = models.ForeignKey(Terminal, related_name='routes_to', 
                                  on_delete=models.CASCADE, verbose_name="مقصد")
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, verbose_name="شرکت")
    bus_type = models.CharField(max_length=20, choices=[
        ('standard', 'معمولی'),
        ('luxury', 'لوکس'),
        ('vip', 'وی آی پی'),
    ], verbose_name="نوع اتوبوس")
    base_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت پایه")
    distance_km = models.PositiveIntegerField(verbose_name="مسافت (کیلومتر)")
    estimated_duration = models.DurationField(verbose_name="مدت زمان تقریبی سفر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مسیر"
        verbose_name_plural = "مسیرها"
        unique_together = ('origin', 'destination', 'company', 'bus_type')
        ordering = ['origin', 'destination']

    def clean(self):
        if self.origin == self.destination:
            raise ValidationError("مبدا و مقصد نمی‌توانند یکسان باشند")

    def __str__(self):
        return f"{self.origin.city.name} → {self.destination.city.name} ({self.company.name}, {self.bus_type})"

    @property
    def route_name(self):
        return f"{self.origin.city.name} - {self.destination.city.name}"