from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    length = models.CharField(max_length=16)
    mass = models.CharField(max_length=16)
    energy = models.CharField(max_length=16)
