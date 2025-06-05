from django.db import models

# Create your models here.

class Buscompany(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام شرکت')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=15, verbose_name='تلفن')
    address = models.TextField(verbose_name='آدرس')



    class Meta:
        verbose_name = 'شرکت اتوبوسرانی'
        verbose_name_plural = 'شرکت‌های اتوبوسرانی'

    def __str__(self):
        return self.name

