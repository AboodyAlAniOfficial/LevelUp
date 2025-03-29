from django.db import models
from django.contrib.auth.models import User

class PredefinedDatabase(models.Model):
    Food_id = models.IntegerField(primary_key=True)
    Food = models.CharField(max_length=255)
    Measure = models.CharField(max_length=100)
    Grams = models.IntegerField()
    Calories = models.IntegerField(null=True, blank=True)
    Proteins = models.IntegerField(null=True, blank=True)
    Fats = models.IntegerField(null=True, blank=True)
    Carbs = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'fooddata'

    def __str__(self):
        return self.Food

class LoggedMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loggedmeal'

    def __str__(self):
        return f"{self.meal_name} (User: {self.user.username})"

class FoodItem(models.Model):
    meal = models.ForeignKey(LoggedMeal, related_name='foods', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    calories = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fats = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.food_name} for meal {self.meal.meal_name}"
