from django.http import HttpResponse
from rest_framework import viewsets, filters
from city.models import City, Province, Terminal
from .serializers import CitySerializer, ProvinceSerializer, TerminalSerializer
from django_filters.rest_framework import DjangoFilterBackend


def view(request):
    return HttpResponse('Hello World')


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'province']
    search_fields = ['name', 'province__name']
    ordering_fields = ['name', 'province__name']
    ordering = ['name']

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'city__name']
    search_fields = ['name', 'city__name']
    ordering_fields = ['name', 'city__name']
    ordering = ['name']
    