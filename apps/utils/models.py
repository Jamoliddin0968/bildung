# myapp/models.py
from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    order_number = models.IntegerField(default=0)

    class Meta:
        ordering = ['order_number']

    def __str__(self):
        return self.title
