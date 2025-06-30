from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from routes.models import Route
from .serializers import RouteSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['origin', 'destination', 'company', 'bus_type', 'is_active']
    search_fields = ['origin__name', 'destination__name', 'company__name']
    ordering_fields = ['base_price', 'distance_km', 'estimated_duration', 'created_at']
    ordering = ['created_at']
