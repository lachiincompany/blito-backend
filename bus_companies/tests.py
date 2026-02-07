from django.urls import get_resolver
from rest_framework import status
from rest_framework.test import APITestCase

from bus_companies.models import BusCompany
from fleet.models import Fleet


def find_url_regex_contains(text):
    """
    Finds first url pattern string that contains `text`.
    Returns it with leading slash.
    """
    r = get_resolver()

    patterns = []

    def walk(ps, prefix=""):
        for p in ps:
            if hasattr(p, "url_patterns"):
                walk(p.url_patterns, prefix + str(p.pattern))
            else:
                patterns.append(prefix + str(p.pattern))

    walk(r.url_patterns)

    hits = [p for p in patterns if text in p]
    if not hits:
        raise AssertionError(f"Could not find url containing: {text}")

    u = sorted(hits, key=len)[0]
    if not u.startswith("/"):
        u = "/" + u
    return u


def normalize_list_url(regex_pattern):
    """
    Converts:
      /bus_companies/api/v1/^companies/$
    to:
      /bus_companies/api/v1/companies/
    """
    u = regex_pattern
    u = u.replace("^", "")
    u = u.replace("$", "")
    # remove escaping if any
    u = u.replace("\\", "")
    return u


def normalize_detail_tpl(regex_pattern):
    """
    Converts:
      /bus_companies/api/v1/^companies/(?P<pk>[^/.]+)/$
    to:
      /bus_companies/api/v1/companies/{pk}/
    """
    u = regex_pattern
    u = u.replace("^", "")
    u = u.replace("$", "")
    u = u.replace("\\", "")
    u = u.replace("(?P<pk>[^/.]+)", "{pk}")
    return u


class BusCompanyAPITests(APITestCase):
    def setUp(self):
        list_regex = find_url_regex_contains("^companies/$")
        detail_regex = find_url_regex_contains("^companies/(?P<pk>[^/.]+)/$")

        self.list_url = normalize_list_url(list_regex)
        self.detail_tpl = normalize_detail_tpl(detail_regex)

        self.c1 = BusCompany.objects.create(
            name="Company A", email="a@co.com", phone="021111111", address="Addr A"
        )
        self.c2 = BusCompany.objects.create(
            name="Company B", email="b@co.com", phone="021222222", address="Addr B"
        )

        # برای active_buses_count
        Fleet.objects.create(
            company=self.c1,
            bus_number="BUS-100",
            license_plate="11الف111-11",
            model="X",
            brand="Y",
            year=2020,
            capacity=40,
            bus_type="standard",
            is_active=True,
        )
        Fleet.objects.create(
            company=self.c1,
            bus_number="BUS-101",
            license_plate="11الف222-11",
            model="X2",
            brand="Y2",
            year=2021,
            capacity=45,
            bus_type="vip",
            is_active=False,
        )

    def detail_url(self, obj):
        return self.detail_tpl.format(pk=obj.pk)

    def test_list_bus_companies(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 2)
        self.assertIn("active_buses_count", res.data[0])

    def test_create_bus_company_success(self):
        res = self.client.post(
            self.list_url,
            {
                "name": "Company C",
                "email": "c@co.com",
                "phone": "021333333",
                "address": "Addr C",
                "active_buses_count": 999, 
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        obj = BusCompany.objects.get(name="Company C")
        self.assertEqual(obj.active_buses_count, 0)

    def test_retrieve_update_delete_bus_company(self):
        url = self.detail_url(self.c1)

        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        p = self.client.patch(url, {"address": "New Address"}, format="json")
        self.assertEqual(p.status_code, status.HTTP_200_OK)

        d = self.client.delete(url)
        self.assertEqual(d.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_by_email(self):
        res = self.client.get(self.list_url, {"email": "a@co.com"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_search_by_name(self):
        res = self.client.get(self.list_url, {"search": "Company B"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_ordering_by_name(self):
        res = self.client.get(self.list_url, {"ordering": "-name"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 2)
