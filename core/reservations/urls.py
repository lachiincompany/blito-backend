from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('reservations.api.v1.urls')),
]
