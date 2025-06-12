from django.http import HttpResponse
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from bus_companies.models import BusCompany
from .serializers import BusCompanySerializer


def view(request):
    return HttpResponse('Hello World')

class BusCompanyViewSet(viewsets.ModelViewSet):
    queryset = BusCompany.objects.all()
    serializer_class = BusCompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['name', 'email']
    
    search_fields = ['name', 'email', 'phone', 'address']
    ordering_fields = ['name', 'email', 'active_buses_count']
    ordering = ['name']  