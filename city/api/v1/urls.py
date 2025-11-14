from django.urls import path , include
from .views import CityViewSet, ProvinceViewSet, TerminalViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('cities', CityViewSet, basename='city')
router.register('provinces', ProvinceViewSet, basename='province')
router.register('terminals', TerminalViewSet, basename='terminal')

urlpatterns = [
    path('', include(router.urls)),
]
