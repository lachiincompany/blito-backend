from django.db import models

# Create your models here.

class Buscompany(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام شرکت')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=15, verbose_name='تلفن')
    address = models.TextField(verbose_name='آدرس')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='امتیاز')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='تعداد امتیازها')


    class Meta:
        verbose_name = 'شرکت اتوبوسرانی'
        verbose_name_plural = 'شرکت‌های اتوبوسرانی'

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return f"{self.rating}/5.0"

    @property  
    def rating_display(self):
        return "⭐" * int(self.rating)