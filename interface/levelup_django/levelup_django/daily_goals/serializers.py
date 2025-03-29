from rest_framework import serializers
from .models import daily_goals
from meals.models import LoggedMeal
from accounts.models import User, HealthData

class Daily_GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = daily_goals
        fields = ['goal_id', 'user','target_weight', 'daily_calorie_goal', 'daily_steps_goal', 'created_at']

class calorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = daily_goals
        fields = ['daily_calorie_goal']

class mealSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = LoggedMeal
        fields = ['meal_name', 'calories']

class dictionarySerializer(serializers.Serializer):

    breakfast = mealSerializer(required=False)
    lunch = mealSerializer(required=False)
    dinner = mealSerializer(required=False)

class stepGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = daily_goals
        fields = ['daily_steps_goal']

class weightGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = daily_goals
        fields = ['target_weight']

class userSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'user_id']
    def get_user_id(self, obj):

        return obj.pk

class healthDataSerializer(serializers.ModelSerializer):
       
       class Meta:
           model = HealthData
           fields = ['mass_kg']