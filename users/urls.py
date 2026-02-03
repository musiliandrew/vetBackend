from django.urls import path
from .views import register_user, login_user, get_profile, send_otp, verify_otp

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', get_profile, name='profile'),
    path('send-otp/', send_otp, name='users_send_otp'),
    path('verify-otp/', verify_otp, name='users_verify_otp'),
]
