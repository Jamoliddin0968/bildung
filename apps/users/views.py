from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, CustomUser
from .serializers import OTPGenerationSerializer, OTPVerificationSerializer


class OTPGenerationAPIView(GenericAPIView):
    serializer_class = OTPGenerationSerializer

    def post(self, request, *args, **kwargs):
        serializer = OTPGenerationSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'OTP sent', 'otp_code': result['otp_code']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationAPIView(GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            serializer.update_user(user)
            OTP.objects.filter(
                user=user, code=request.data['otp_code']).delete()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'OTP verified successfully',
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
