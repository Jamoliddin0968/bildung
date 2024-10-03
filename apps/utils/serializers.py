# myapp/serializers.py
from rest_framework import serializers

from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'is_active', 'order_number']
