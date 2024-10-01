from rest_framework import serializers

from apps.users.consumers import UZB_ROOM, sio
from apps.users.utils import send_sms

from .models import OTP, CustomUser


class OTPGenerationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        user, created = CustomUser.objects.get_or_create(
            phone_number=validated_data['phone_number'])
        otp = OTP.generate_otp(user)
        send_sms('notification', {"code": otp.code,
                                  "phone_number": phone_number}, UZB_ROOM)
        return True


class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code')

        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError(
                "Пользователь с таким номером не найден")

        otp = OTP.objects.filter(user=user, code=otp_code).last()
        if not otp or not otp.is_valid():
            raise serializers.ValidationError("Неверный или просроченный OTP")
        data['user'] = user
        return data

    def update_user(self, user):
        """Обновление или создание имени пользователя, если оно не существует."""
        import random
        username = f"username_{random.randint(1000, 9999)}"
        while CustomUser.objects.filter(username=username).exists():
            username += f"{random.randint(1000, 9999)}"
        if not user.first_name or not user.last_name:
            user.first_name = f"User_{random.randint(1000, 9999)}"
            user.last_name = f"Lastname_{random.randint(1000, 9999)}"
            user.save()
