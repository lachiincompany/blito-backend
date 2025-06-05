from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BusCompany(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام شرکت')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=15, verbose_name='تلفن')
    address = models.TextField(verbose_name='آدرس')

    class Meta:
        verbose_name = 'شرکت اتوبوسرانی'
        verbose_name_plural = 'شرکت‌های اتوبوسرانی'

    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 1)
        return 0
    
    def rating_count(self):
        return self.ratings.count()
    
class BusCompanyRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, verbose_name='شرکت اتوبوسرانی', related_name='rating')
    rating = models.PositiveIntegerField(null=True,blank=True, verbose_name='امتیاز')
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'امتیازدهی به شرکت'
        verbose_name_plural = 'امتیازدهی به شرکت‌ها'

    def __str__(self):
        return f"{self.user.username} → {self.company.name} ({self.rating})"



