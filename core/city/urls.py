from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('city.api.v1.urls')),
]
