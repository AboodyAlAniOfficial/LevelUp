from django.db import models

# Create your models here.

class Unit(models.Model):
    username = models.CharField(max_length=150)
    length = models.CharField(max_length=16)
    mass = models.CharField(max_length=16)
    energy = models.CharField(max_length=16)
