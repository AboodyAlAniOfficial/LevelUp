from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PredefinedMeal(models.Model):
    foodid = models.IntegerField(primary_key=True)
    fooddescription = models.CharField(max_length=255)

    class Meta:
        db_table = 'fooddata'
        managed = False 

    def __str__(self):
        return self.fooddescription


class LoggedMeal(models.Model):
    meal_id = models.AutoField(primary_key=True, db_column='meal_id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='logged_meals'
    )
    meal_name = models.CharField(max_length=255, db_column='meal_name')
    calories = models.IntegerField(db_column='calories')
    protein = models.IntegerField(db_column='protein')
    carbs = models.IntegerField(db_column='carbs')
    fats = models.IntegerField(db_column='fats')
    description = models.TextField(db_column='description', blank=True, null=True)

    class Meta:
        db_table = 'meals'
        managed = False  # We don't want Django to create/alter 'meals'

    def __str__(self):
        return f"{self.meal_name} (User: {self.user.username})"
