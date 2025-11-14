from django.urls import path, include

app_name = 'bus_companies'

urlpatterns = [
    path('api/v1/', include('bus_companies.api.v1.urls')),
]
