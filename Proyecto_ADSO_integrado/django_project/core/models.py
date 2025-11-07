from django.db import models
class Address(models.Model):
    calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
