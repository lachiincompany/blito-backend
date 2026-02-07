from django.urls import reverse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Province, City, Terminal


class ProvinceAPITests(APITestCase):
    def setUp(self):
        self.province = Province.objects.create(name="تهران")
        self.list_url = reverse("province-list")

    def test_list_provinces(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 1)
        self.assertIn("name", res.data[0])

    def test_create_province(self):
        res = self.client.post(self.list_url, {"name": "البرز"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Province.objects.filter(name="البرز").exists())

    def test_create_province_duplicate_name_should_fail(self):
        res = self.client.post(self.list_url, {"name": "تهران"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_update_delete_province(self):
        detail_url = reverse("province-detail", args=[self.province.id])

        r = self.client.get(detail_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], "تهران")

        p = self.client.patch(detail_url, {"name": "تهران بزرگ"}, format="json")
        self.assertEqual(p.status_code, status.HTTP_200_OK)
        self.province.refresh_from_db()
        self.assertEqual(self.province.name, "تهران بزرگ")

        d = self.client.delete(detail_url)
        self.assertEqual(d.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Province.objects.filter(id=self.province.id).exists())


class CityAPITests(APITestCase):
    def setUp(self):
        self.province1 = Province.objects.create(name="فارس")
        self.province2 = Province.objects.create(name="اصفهان")

        City.objects.create(name="شیراز", province=self.province1, is_active=True)
        City.objects.create(name="کازرون", province=self.province1, is_active=False)
        City.objects.create(name="اصفهان", province=self.province2, is_active=True)

        self.list_url = reverse("city-list")

    def test_list_cities(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_create_city_raises_integrity_error_current_behavior(self):
        """
        در کد فعلی CitySerializer، فیلد province read_only است
        و داده‌ی province از درخواست وارد validated_data نمی‌شود.
        بنابراین create باعث NULL شدن province_id و IntegrityError می‌شود.
        """
        with self.assertRaises(IntegrityError):
            self.client.post(
                self.list_url,
                {"name": "مرودشت", "province": self.province1.id, "is_active": True},
                format="json",
            )

    def test_filter_by_province_name_current_behavior(self):
        """
        در کد فعلی CityViewSet، filterset_fields شامل province__name نیست
        بنابراین این فیلتر اعمال نمی‌شود و همه رکوردها برمی‌گردد.
        """
        res = self.client.get(self.list_url, {"province__name": "فارس"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)  # رفتار فعلی

    def test_filter_by_is_active_current_behavior(self):
        """
        در کد فعلی CityViewSet، filterset_fields شامل is_active نیست
        بنابراین این فیلتر اعمال نمی‌شود و همه رکوردها برمی‌گردد.
        """
        res = self.client.get(self.list_url, {"is_active": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)  # رفتار فعلی

    def test_search_cities(self):
        res = self.client.get(self.list_url, {"search": "فارس"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


class TerminalAPITests(APITestCase):
    def setUp(self):
        self.province = Province.objects.create(name="خراسان رضوی")
        self.city = City.objects.create(name="مشهد", province=self.province, is_active=True)

        self.terminal = Terminal.objects.create(
            city=self.city,
            name="پایانه امام رضا",
            address="بزرگراه کلانتری",
            phone="05112345678",
            is_active=True,
        )

        self.list_url = reverse("terminal-list")

    def test_list_terminals(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], self.terminal.name)

    def test_create_terminal_raises_integrity_error_current_behavior(self):
        """
        در کد فعلی TerminalSerializer، فیلد city read_only است
        و city از درخواست وارد validated_data نمی‌شود.
        بنابراین create باعث NULL شدن city_id و IntegrityError می‌شود.
        """
        with self.assertRaises(IntegrityError):
            self.client.post(
                self.list_url,
                {
                    "city": self.city.id,
                    "name": "پایانه معراج",
                    "address": "بلوار توس",
                    "phone": "05199999999",
                    "is_active": True,
                },
                format="json",
            )

    def test_unique_terminal_name_per_city_db_level(self):
        with self.assertRaises(IntegrityError):
            Terminal.objects.create(city=self.city, name="پایانه امام رضا")

    def test_search_terminals(self):
        res = self.client.get(self.list_url, {"search": "مشهد"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
