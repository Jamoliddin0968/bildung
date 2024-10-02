# Create your models here.
import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)


class OTP(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=2)

    @staticmethod
    def generate_otp(user):
        code = f'{random.randint(1000, 9999)}'
        code = '1111'
        otp = OTP.objects.create(user=user, code=code)
        return otp
