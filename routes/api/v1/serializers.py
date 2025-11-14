from rest_framework import serializers
from routes.models import Route

class RouteSerializer(serializers.ModelSerializer):
    origin = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()
    company = serializers.StringRelatedField()
    class Meta:
        model = Route
        fields = [
            'id',
            'origin',
            'destination',
            'company',
            'bus_type',
            'base_price',
            'distance_km',
            'estimated_duration',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['created_at']
