from django.urls import path

from .views import OTPGenerationAPIView, OTPVerificationAPIView

urlpatterns = [
    path('phone-number/', OTPGenerationAPIView.as_view(), name='otp_generate'),
    path('otp/verify/', OTPVerificationAPIView.as_view(), name='otp_verify'),
]
