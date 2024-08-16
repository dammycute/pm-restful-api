from django.urls import path

from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name= 'register'),
    path('activate', ActivationView.as_view(), name= 'activate'),
    path('password-reset', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm', PasswordResetView.as_view(), name='password_reset_confirm'),
    path('profile', ProfileUpdateView.as_view(), name='profile_update')
]