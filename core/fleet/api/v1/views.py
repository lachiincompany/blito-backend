# fleet/views.py
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from fleet.models import Fleet
from .serializers import FleetSerializer


class FleetViewSet(ModelViewSet):
    queryset = Fleet.objects.select_related('company', 'driver').all()
    serializer_class = FleetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # فیلترهای دقیق
    filterset_fields = {
        'company': ['exact'],
        'bus_type': ['exact'],        # standard, vip, luxury
        'has_wifi': ['exact'],
        'has_ac': ['exact'],
        'has_tv': ['exact'],
        'has_charging': ['exact'],
        'has_blanket': ['exact'],
        'has_food_service': ['exact'],
        'is_active': ['exact'],
    }

    # جستجو بر اساس شماره اتوبوس، برند و مدل
    search_fields = ['bus_number', 'brand', 'model', 'license_plate']

    # مرتب‌سازی
    ordering_fields = ['year', 'capacity', 'bus_number']
