from rest_framework import serializers
from .models import daily_goals

class Daily_GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = daily_goals
        fields = ['goal_id', 'user','target_weight', 'daily_calorie_goal', 'daily_steps_goal', 'created_at']

class calorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = daily_goals
        fields = ['daily_calorie_goal']