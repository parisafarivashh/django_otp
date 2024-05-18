from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authorize.views import TokenController, OtpGeneratorController, UserRegisterController


urlpatterns = [
    path(
        'token/',
        TokenController.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'otp/',
        OtpGeneratorController.as_view(),
        name='create otp',
    ),
    path(
        'register/',
        UserRegisterController.as_view(),
        name='register user',
    ),
]
