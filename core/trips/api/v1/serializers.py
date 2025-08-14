from rest_framework import serializers
from trips.models import Trip
from routes.api.v1.serializers import RouteSerializer
from fleet.api.v1.serializers import FleetSerializer
class TripSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    fleet = FleetSerializer(source='bus', read_only=True)
    class Meta:
        model = Trip
        fields = [
            'id',
            'route',
            'fleet',
            'departure_datetime',
            'arrival_datetime',
            'current_price',
            'status',
            'driver_name',
            'driver_phone',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']