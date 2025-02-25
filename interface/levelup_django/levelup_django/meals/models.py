# meals/models.py

from django.db import models
# If you have a custom user model:
# from accounts.models import User
# If using Django's default user model:
from django.contrib.auth.models import User

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    calories = models.PositiveIntegerField()
    macronutrients = models.JSONField()  # e.g. {"fats": 10, "carbs": 20, "proteins": 15}
    ingredients = models.JSONField()      # e.g. [{"name": "apple", "weight": 150}, ...]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.meal_name} ({self.calories} kcal)"
