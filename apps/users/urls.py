from django.urls import path

from .views import (DeleteAccountView, OTPGenerationAPIView,
                    OTPVerificationAPIView, UserMeView)

urlpatterns = [
    path('phone-number/', OTPGenerationAPIView.as_view(), name='otp_generate'),
    path('otp/verify/', OTPVerificationAPIView.as_view(), name='otp_verify'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]
