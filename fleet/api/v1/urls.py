from django.urls import path , include
from .views import FleetViewSet
from rest_framework.routers import DefaultRouter


fleets = DefaultRouter()
fleets.register('fleets', FleetViewSet, basename='fleets')


urlpatterns = [
    path('', include(fleets.urls)),
]
