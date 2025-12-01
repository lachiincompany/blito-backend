from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payments.api.v1.views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('api/', include(router.urls)),
]

