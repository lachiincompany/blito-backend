from rest_framework import serializers
from trips.models import Trip

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            'id',
            'route',
            'bus',
            'departure_datetime',
            'arrival_datetime',
            'current_price',
            'status',
            'driver_name',
            'driver_phone',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']