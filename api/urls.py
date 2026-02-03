from django.urls import path
from .views import health_check, send_otp, verify_otp

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]
