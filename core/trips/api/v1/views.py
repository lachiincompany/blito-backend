# trips/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from trips.models import Trip
from .serializers import TripSerializer

class TripViewSet(ModelViewSet):
    queryset = Trip.objects.select_related('route__origin', 'route__destination', 'bus', 'route__company').all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'route__origin__id': ['exact'],
        'route__destination__id': ['exact'],
        'departure_datetime': ['date'],
    }
    ordering_fields = ['departure_datetime', 'current_price']
