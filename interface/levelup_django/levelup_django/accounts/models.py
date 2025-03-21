from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    length = models.CharField(max_length=16)
    mass = models.CharField(max_length=16)
    energy = models.CharField(max_length=16)

class Preferences(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    privacy = models.CharField(max_length=16)

class HealthData(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    height_m = models.FloatField(null=True)
    mass_kg = models.FloatField(null=True)
    age_yr = models.FloatField(null=True)
    sex = models.CharField(max_length=16)
