from django.urls import path, include

app_name = 'fleet'

urlpatterns = [
    path('api/v1/', include('fleet.api.v1.urls')),
]
