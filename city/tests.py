from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Province, City, Terminal

class ProvinceAPITests(APITestCase):
    def setUp(self):
        """ این متد قبل از هر تست اجرا می‌شود و داده‌های اولیه را ایجاد می‌کند """
        self.province = Province.objects.create(name="تهران")

    def test_list_provinces(self):
        """ تست دریافت لیست استان‌ها """
        url = reverse('province-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.province.name)

    def test_create_province(self):
        """ تست ایجاد یک استان جدید """
        url = reverse('province-list')
        data = {'name': 'البرز'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Province.objects.count(), 2)
        self.assertEqual(Province.objects.get(id=response.data['id']).name, 'البرز')


class CityAPITests(APITestCase):
    def setUp(self):
        self.province1 = Province.objects.create(name="فارس")
        self.province2 = Province.objects.create(name="اصفهان")
        self.city1 = City.objects.create(name="شیراز", province=self.province1)
        self.city2 = City.objects.create(name="کازرون", province=self.province1)
        self.city3 = City.objects.create(name="اصفهان", province=self.province2)

    def test_list_cities(self):
        """ تست دریافت لیست شهرها """
        url = reverse('city-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_city(self):
        """ تست ایجاد یک شهر جدید """
        url = reverse('city-list')
        # برای ایجاد شهر، باید id استان را ارسال کنیم
        data = {'name': 'مرودشت', 'province': self.province1.id}
        response = self.client.post(url, data, format='json')
        # در پاسخ سریالایزر، نام استان نمایش داده می‌شود، نه id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), 4)
        self.assertEqual(response.data['province'], self.province1.name)

    def test_filter_cities_by_province(self):
        """ تست فیلتر کردن شهرها بر اساس استان """
        url = reverse('city-list')
        # فیلتر بر اساس نام استان
        response = self.client.get(url, {'province__name': 'فارس'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'شیراز')


class TerminalAPITests(APITestCase):
    def setUp(self):
        self.province = Province.objects.create(name="خراسان رضوی")
        self.city = City.objects.create(name="مشهد", province=self.province)
        self.terminal = Terminal.objects.create(
            city=self.city,
            name="پایانه امام رضا",
            address="بزرگراه کلانتری"
        )

    def test_list_terminals(self):
        """ تست دریافت لیست ترمینال‌ها """
        url = reverse('terminal-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.terminal.name)

    def test_create_terminal(self):
        """ تست ایجاد یک ترمینال جدید """
        url = reverse('terminal-list')
        data = {
            'city': self.city.id,
            'name': 'پایانه معراج',
            'address': 'بلوار توس',
            'phone': '05112345678'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Terminal.objects.count(), 2)
        # در پاسخ سریالایزر، نام شهر نمایش داده می‌شود
        self.assertEqual(response.data['city'], self.city.name)
