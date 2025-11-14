# trips/serializers.py
from rest_framework import serializers
from trips.models import Trip
from routes.api.v1.serializers import RouteSerializer
from fleet.models import Fleet  # مسیر مدل ناوگان
from bus_companies.models import BusCompany


class FleetSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    facilities = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = [
            'id',
            'company_name',
            'bus_number',
            'license_plate',
            'model',
            'brand',
            'year',
            'capacity',
            'bus_type',
            'facilities',
            'image',
            'interior_image'
        ]

    def get_facilities(self, obj):
        return obj.get_facilities()

