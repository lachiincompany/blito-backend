from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from city.models import Terminal
from bus_companies.models import BusCompany
from fleet.models import Fleet
from accounts.models import Profile
from routes.models import Route
from trips.models import Trip
import random

class Command(BaseCommand):
    help = "Seed database with Routes and Trips"

    def handle(self, *args, **kwargs):
        terminal_ids = list(range(1, 61))
        company_ids = list(range(50, 80))
        driver_ids = list(range(97, 107))
        bus_types = ['standard', 'luxury', 'vip']

        def get_random_terminal(exclude_id=None):
            tid = random.choice(terminal_ids)
            while tid == exclude_id:
                tid = random.choice(terminal_ids)
            return Terminal.objects.get(id=tid)

        def get_random_company():
            return BusCompany.objects.get(id=random.choice(company_ids))

        def get_random_driver():
            return Profile.objects.get(id=random.choice(driver_ids))

        def get_matching_bus(company, bus_type):
            possible_buses = Fleet.objects.filter(company=company, bus_type=bus_type, is_active=True)
            if not possible_buses.exists():
                raise ValueError(f"No matching bus for company {company.id} and type {bus_type}")
            return random.choice(possible_buses)

        routes_created = []
        for i in range(20):
            origin = get_random_terminal()
            destination = get_random_terminal(exclude_id=origin.id)
            company = get_random_company()
            bus_type = random.choice(bus_types)
            base_price = random.randint(100000, 1000000)
            distance_km = random.randint(100, 1000)
            estimated_duration = timedelta(hours=distance_km // 100)

            if not Route.objects.filter(origin=origin, destination=destination, company=company, bus_type=bus_type).exists():
                route = Route.objects.create(
                    origin=origin,
                    destination=destination,
                    company=company,
                    bus_type=bus_type,
                    base_price=base_price,
                    distance_km=distance_km,
                    estimated_duration=estimated_duration,
                    is_active=True
                )
                route.clean()
                route.save()
                routes_created.append(route)
                self.stdout.write(self.style.SUCCESS(f"Created Route: {route}"))

        for route in routes_created:
            for j in range(5):
                now = datetime(2025, 8, 20, tzinfo=timezone.utc)
                delta_days = random.randint(0, 7)
                delta_hours = random.randint(0, 23)
                delta_minutes = random.randint(0, 59)
                departure = now + timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)

                arrival = departure + route.estimated_duration + timedelta(minutes=random.randint(30, 60))

                bus = get_matching_bus(route.company, route.bus_type)
                driver = get_random_driver()
                current_price = route.base_price + random.randint(-50000, 50000)

                trip = Trip(
                    route=route,
                    bus=bus,
                    departure_datetime=departure,
                    arrival_datetime=arrival,
                    current_price=current_price,
                    status='SCHEDULED',
                    driver_name=driver,
                )
                trip.clean()
                trip.save()
                self.stdout.write(self.style.SUCCESS(f"Created Trip: {trip}"))