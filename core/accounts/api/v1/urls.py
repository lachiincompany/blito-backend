from django.urls import path 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    CustomTokenObtainPairView,
    ChangePasswordView,
    ProfileView,
    RegisterView,
    LogoutView,
)
urlpatterns = [
    path('api/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/change_password', ChangePasswordView.as_view(), name='change_password'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/profile', ProfileView.as_view() , name= "profile"),
    path('api/register', RegisterView.as_view(), name="register"),
    path('api/logout/', LogoutView.as_view(), name="Logout"),
]
