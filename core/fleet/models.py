from django.db import models
from bus_companies.models import BusCompany
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
# Create your models here.

class Fleet(models.Model):
    BUS_TYPE_CHOICES = [
        ('standard', 'معمولی'),
        ('luxury', 'لوکس'),
        ('vip', 'وی آی پی'),
    ]

    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, verbose_name='شرکت اتوبوسرانی', related_name='fleet')
    bus_number = models.CharField(max_length=20, unique=True, verbose_name='شماره اتوبوس')
    license_plate = models.CharField(max_length=15, unique=True, verbose_name='پلاک')
    model = models.CharField(max_length=50, verbose_name='مدل')
    brand = models.CharField(max_length=50, verbose_name='برند')
    year = models.PositiveIntegerField(
        validators= [
            MaxValueValidator(2023),
            MinValueValidator(1980),
        ],
        verbose_name='سال تولید'
    )
    capacity = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(60),
            MinValueValidator(10)
        ],
        verbose_name='ظرفیت'
    )
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES, default='standard', verbose_name='نوع اتوبوس')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='راننده', related_name='fleet')



    has_wifi = models.BooleanField(default=False, verbose_name=' وای فای')
    has_ac = models.BooleanField(default=False, verbose_name='کولر')
    has_tv = models.BooleanField(default=False, verbose_name='تلویزیون')
    has_charging = models.BooleanField(default=False, verbose_name='شارژر')
    has_blanket = models.BooleanField(default=False, verbose_name='پتو')
    has_food_service = models.BooleanField(default=False, verbose_name='سرویس غذا')


    image = models.ImageField(upload_to='fleet_images/', verbose_name='تصویر', blank=True, null=True)
    interior_image = models.ImageField(upload_to='fleet_images/', null=True, blank=True, verbose_name='تصویر داخلی')


    class Meta:
        verbose_name = 'اتوبوس ناوگان'
        verbose_name_plural = 'ناوگان اتوبوس‌ها'
        ordering = ['company', 'bus_number']

    def __str__(self):
        return f"{self.company.name} - {self.bus_number} ({self.license_plate})"
    

    def get_facilities(self):
        facilities = []
        if self.has_wifi:
            facilities.append('وای‌فای رایگان')
        if self.has_ac:
            facilities.append('کولر')
        if self.has_toilet:
            facilities.append('سرویس بهداشتی')
        if self.has_tv:
            facilities.append('تلویزیون')
        if self.has_charging:
            facilities.append('شارژر موبایل')
        if self.has_music:
            facilities.append('سیستم صوتی')
        if self.has_blanket:
            facilities.append('پتو')
        if self.has_food_service:
            facilities.append('سرویس غذا')
        return facilities
    
    def get_capacity(self):
        return f'{self.capacity} نفر'