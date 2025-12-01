from django.db.models.signals import post_save
from django.dispatch import receiver
from trips.models import Trip
from seat.models import Seat

@receiver(post_save, sender=Trip)
def create_seats_for_trip(sender, instance, created, **kwargs):
    if created:
        capacity = instance.bus.capacity
        for i in range(1, capacity + 1):
            Seat.objects.get_or_create(
                trip=instance,
                seat_number=i
            )
