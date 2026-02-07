from django.urls import get_resolver
from rest_framework import status
from rest_framework.test import APITestCase

from bus_companies.models import BusCompany
from fleet.models import Fleet
from django.urls import get_resolver

def drf_list_url_for(basename_hint="fleet"):
    resolver = get_resolver()
    urls = []

    def walk(patterns, prefix=""):
        for p in patterns:
            if hasattr(p, "url_patterns"):
                walk(p.url_patterns, prefix + str(p.pattern))
            else:
                urls.append(prefix + str(p.pattern))

    walk(resolver.url_patterns)

    candidates = []
    for u in urls:
        u2 = u if u.startswith("/") else "/" + u
        if "admin" in u2 or "login" in u2:
            continue
        if "<" in u2 or "{" in u2:  
            continue
        if not u2.endswith("/"):
            continue
        if basename_hint in u2:
            candidates.append(u2)

    if not candidates:
        fleet_like = [u for u in urls if basename_hint in u]
        raise AssertionError("No list URL found. Fleet-like urls:\n" + "\n".join(sorted(fleet_like)))

    return sorted(candidates, key=len)[0]


def drf_detail_template_for(basename_hint="fleet"):
    """
    Returns a detail template like:
      /api/v1/fleet/{id}/
    or if lookup is string:
      /api/v1/fleet/{lookup}/
    based on the real URL pattern.
    """
    resolver = get_resolver()
    urls = []

    def walk(patterns, prefix=""):
        for p in patterns:
            if hasattr(p, "url_patterns"):
                walk(p.url_patterns, prefix + str(p.pattern))
            else:
                urls.append(prefix + str(p.pattern))

    walk(resolver.url_patterns)

    detail_candidates = []
    for u in urls:
        u2 = u if u.startswith("/") else "/" + u
        if "admin" in u2 or "login" in u2:
            continue
        if basename_hint not in u2:
            continue
        if "<" not in u2 and "{" not in u2:
            continue
        if not u2.endswith("/"):
            continue
        detail_candidates.append(u2)

    if not detail_candidates:
        fleet_like = [u for u in urls if basename_hint in u]
        raise AssertionError("No detail URL found. Fleet-like urls:\n" + "\n".join(sorted(fleet_like)))

    u = sorted(detail_candidates, key=len)[0]

    import re
    u = re.sub(r"<[^:]+:[^>]+>", "{lookup}", u)
    u = re.sub(r"<[^>]+>", "{lookup}", u)
    return u


def drf_list_url_for(basename_hint="fleet"):
    resolver = get_resolver()
    urls = []

    def walk(patterns, prefix=""):
        for p in patterns:
            if hasattr(p, "url_patterns"):
                walk(p.url_patterns, prefix + str(p.pattern))
            else:
                urls.append(prefix + str(p.pattern))

    walk(resolver.url_patterns)

    candidates = []
    for u in urls:
        u2 = u if u.startswith("/") else "/" + u
        if "admin" in u2 or "login" in u2:
            continue
        if "<" in u2 or "{" in u2:
            continue
        if not u2.endswith("/"):
            continue
        if basename_hint in u2:
            candidates.append(u2)

    if not candidates:
        fleet_like = [u for u in urls if basename_hint in u]
        raise AssertionError("No list URL found. Fleet-like urls:\n" + "\n".join(sorted(fleet_like)))

    return sorted(candidates, key=len)[0]


class FleetAPITests(APITestCase):
    def setUp(self):
        self.company1 = BusCompany.objects.create(name="Co1", email="co1@x.com", phone="0211000", address="A1")
        self.company2 = BusCompany.objects.create(name="Co2", email="co2@x.com", phone="0212000", address="A2")

        self.f1 = Fleet.objects.create(
            company=self.company1,
            bus_number="BUS-1",
            license_plate="11الف111-11",
            model="ModelA",
            brand="BrandA",
            year=2020,
            capacity=40,
            bus_type="standard",
            is_active=True,
            has_wifi=True,
            has_ac=True,
        )
        self.f2 = Fleet.objects.create(
            company=self.company1,
            bus_number="BUS-2",
            license_plate="11الف222-11",
            model="ModelB",
            brand="BrandB",
            year=2019,
            capacity=50,
            bus_type="vip",
            is_active=False,
            has_tv=True,
        )
        self.f3 = Fleet.objects.create(
            company=self.company2,
            bus_number="BUS-3",
            license_plate="11الف333-11",
            model="ModelC",
            brand="BrandC",
            year=2021,
            capacity=45,
            bus_type="luxury",
            is_active=True,
            has_charging=True,
        )

        self.list_url = drf_list_url_for("fleet")

    def _detail_url(self, obj_id):
        return f"{self.list_url}{obj_id}/"

    def test_list_fleet(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_by_company_exact(self):
        res = self.client.get(self.list_url, {"company": self.company1.id})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_by_bus_type(self):
        res = self.client.get(self.list_url, {"bus_type": "vip"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_by_is_active(self):
        res = self.client.get(self.list_url, {"is_active": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_by_facilities_flags(self):
        res = self.client.get(self.list_url, {"has_wifi": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_by_license_plate(self):
        res = self.client.get(self.list_url, {"search": "11الف333"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ordering_by_year(self):
        res = self.client.get(self.list_url, {"ordering": "year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_update_delete_fleet(self):
        detail_url = self._detail_url(self.f1.id)
        r = self.client.get(detail_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
