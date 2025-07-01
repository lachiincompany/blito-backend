from django.urls import path , include
from .views import TripViewSet
from rest_framework.routers import DefaultRouter


trips = DefaultRouter()
trips.register('trips', TripViewSet, basename='trips')


urlpatterns = [
    path('', include(trips.urls)),
]
