import random
import csv
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bus_companies.models import BusCompany
from fleet.models import Fleet
from accounts.models import Profile   # ← اضافه شد

# دریافت مدل کاربر سفارشی
User = get_user_model()


class Command(BaseCommand):
    help = 'Generates fake data for BusCompany and Fleet models'

    def handle(self, *args, **kwargs):
        fake = Faker('fa_IR')
        self.stdout.write(self.style.SUCCESS('شروع فرآیند ساخت داده‌های تستی...'))

        # --- خواندن کاربران راننده ---
        driver_profiles = []
        try:
            with open('accounts_customuser_rows (4).csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('role') == 'driver':
                        try:
                            user = User.objects.get(phone=row['phone'])
                            try:
                                driver_profiles.append(user.profile)
                            except Profile.DoesNotExist:
                                self.stdout.write(
                                    self.style.WARNING(f"کاربر {row['phone']} پروفایل ندارد. صرف‌نظر شد.")
                                )
                        except User.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(f"کاربری با شماره {row['phone']} پیدا نشد. صرف‌نظر شد.")
                            )

            if not driver_profiles:
                self.stdout.write(self.style.ERROR('هیچ راننده‌ای پیدا نشد!'))
                return

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('فایل CSV پیدا نشد!'))
            return

        self.stdout.write(self.style.SUCCESS(f'تعداد {len(driver_profiles)} راننده (Profile) پیدا شد.'))

        # --- ایجاد شرکت‌های اتوبوسرانی ---
        base_names = [
            'سیر و سفر', 'همسفر', 'رویال سفر', 'گیتی پیما',
            'عدل', 'ایران پیما', 'لوان نور', 'آریا سفر', 'آسیا سفر', 'ماهان سفر'
        ]
        suffixes = ["ایرانیان", "گشت", "توس", "پارس", "اندیشه", "نوین", "سریع", "طلایی"]

        bus_companies = []
        used_names = set()

        num_companies = 30  
        for _ in range(num_companies):
            name = None
            while not name or name in used_names:
                base = random.choice(base_names)
                suffix = random.choice(suffixes)
                name = f"{base} {suffix}"
            used_names.add(name)

            company = BusCompany.objects.create(
                name=name,
                email=fake.unique.email(),
                phone=f"09{random.randint(100000000, 999999999)}",
                address=fake.address()
            )
            bus_companies.append(company)

        self.stdout.write(self.style.SUCCESS(f'تعداد {len(bus_companies)} شرکت اتوبوسرانی ساخته شد.'))

        # --- ایجاد اتوبوس‌ها ---
        fleet_count = 0
        bus_brands = ['اسکانیا', 'ولوو', 'مان', 'بنز']
        bus_models = ['مارال', 'درسا', 'B9', 'B12', 'کلاسیک']
        used_numbers = set()

        for company in bus_companies:
            for _ in range(random.randint(5, 15)):
                random_driver_profile = random.choice(driver_profiles)
                bus_number = None
                while not bus_number or bus_number in used_numbers:
                    bus_number = str(random.randint(100, 9999))
                used_numbers.add(bus_number)

                Fleet.objects.create(
                    company=company,
                    bus_number=bus_number,
                    license_plate=f'{random.randint(10, 99)}ع{random.randint(100, 999)}-ایران{random.randint(10, 99)}',
                    model=random.choice(bus_models),
                    brand=random.choice(bus_brands),
                    is_active=True,
                    year=random.randint(2010, 2023),
                    capacity=random.choice([25, 30, 44]),
                    bus_type=random.choice(['standard', 'luxury', 'vip']),
                    driver=random_driver_profile,
                    has_wifi=random.choice([True, False]),
                    has_ac=True,
                    has_tv=random.choice([True, False]),
                    has_charging=random.choice([True, False]),
                    has_blanket=random.choice([True, False]),
                    has_food_service=random.choice([True, False]),
                )
                fleet_count += 1

        self.stdout.write(self.style.SUCCESS(f'تعداد {fleet_count} اتوبوس ساخته شد.'))
        self.stdout.write(self.style.SUCCESS('✅ عملیات با موفقیت پایان یافت.'))
