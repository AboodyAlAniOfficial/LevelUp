from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User




# Create your models here.
class daily_goals(models.Model):
    #Health Goal Id
    goal_id = models.AutoField(primary_key=True)
    #Foreign key from user table
    #TEMPORARILY USING DJANGO USER MODEL
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    #Target weight for user
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    #daily calorie amount/consumption
    daily_calorie_goal = models.IntegerField(validators=[(MinValueValidator(0))], null=True, blank=True)
    #daily steps amount
    daily_steps_goal = models.PositiveIntegerField(validators=[(MinValueValidator(0))], null=True, blank=True)
    #time stamp at time of creation
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'healthgoals'
    def __str__(self):
        return f"Health goal for user Target Weight: {self.target_weight}"
    
