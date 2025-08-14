# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservations.api.v1.views import ReservationViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('api/', include(router.urls)),
]