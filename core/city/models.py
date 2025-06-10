from django.db import models

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام استان")

    
    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استانها"

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام شهر")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="استان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.province})"
    
class Terminal(models.Model):
    city = models.ForeignKey(City, related_name='terminals', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="نام ترمینال")
    address = models.TextField(blank=True, verbose_name="آدرس")
    phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ترمینال"
        verbose_name_plural = "ترمینال‌ها"
        unique_together = ('city', 'name')

    def __str__(self):
        return f"{self.city.name} - {self.name}"