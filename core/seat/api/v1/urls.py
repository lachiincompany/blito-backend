# seats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeatViewSet

router = DefaultRouter()
router.register(r'seats', SeatViewSet, basename='seat')

urlpatterns = [
    path('api/', include(router.urls)),
]