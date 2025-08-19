import random
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser, Profile  
fake = Faker("fa_IR") 


class Command(BaseCommand):
    help = "ایجاد 50 یوزر تستی (مسافر و راننده)"

    def handle(self, *args, **kwargs):
        total_users = 50
        drivers_count = 10 
        customers_count = total_users - drivers_count

        created_users = []

        for _ in range(customers_count):
            self.create_user(role="customer", created_users=created_users)

        for _ in range(drivers_count):
            self.create_user(role="driver", created_users=created_users)

        self.stdout.write(self.style.SUCCESS(f"{len(created_users)} یوزر ساخته شد."))

    def create_user(self, role, created_users):
        full_name = fake.name()
        phone = f"09{random.randint(100000000, 999999999)}"

        user = CustomUser.objects.create_user(
            phone=phone,
            password="test1234", 
            full_name=full_name,
            role=role,
            is_verified=True,
        )

        parts = full_name.split()
        first_name = parts[0]
        last_name = parts[-1] if len(parts) > 1 else ""

        profile = user.profile
        profile.first_name = first_name
        profile.last_name = last_name
        profile.address = fake.address()
        profile.national_id = str(random.randint(1000000000, 9999999999))
        profile.save()

        created_users.append(user)
