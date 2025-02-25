from django.db import models

# Create your models here.
class HealthGoals(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    target_weight = models.FloatField()
    daily_calories = models.PositiveIntegerField()
    daily_steps = models.PositiveIntegerField()

    def __str__(self):
        return self.user_id
