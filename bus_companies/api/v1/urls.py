from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BusCompanyViewSet

router = DefaultRouter()
router.register('companies', BusCompanyViewSet, basename='bus-companies')

urlpatterns = [
    path('', include(router.urls)),
]
