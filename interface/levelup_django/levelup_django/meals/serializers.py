from rest_framework import serializers
from .models import PredefinedMeal, LoggedMeal

class PredefinedMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedMeal
        fields = ['foodid', 'fooddescription']

class LoggedMealSerializer(serializers.ModelSerializer):
    # Use the authenticated user rather than letting the client set this.
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # Accept an extra field for the predefined meal.
    predefined_meal = serializers.PrimaryKeyRelatedField(
        queryset=PredefinedMeal.objects.all(), write_only=True, required=False
    )
    # Accept extra fields that aren't in the model
    meal_type = serializers.CharField(write_only=True, required=False)
    # Map 'notes' to the model's 'description' field and allow it to be blank.
    notes = serializers.CharField(write_only=True, source='description', required=False, allow_blank=True)
    
    # Mark these nutritional fields and meal_name as optional.
    meal_name = serializers.CharField(required=False)
    calories = serializers.IntegerField(required=False)
    protein = serializers.IntegerField(required=False)
    carbs = serializers.IntegerField(required=False)
    fats = serializers.IntegerField(required=False)

    class Meta:
        model = LoggedMeal
        fields = [
            'meal_id', 'user', 'meal_name',
            'calories', 'protein', 'carbs', 'fats',
            'description',  # This field is populated via 'notes'
            'predefined_meal', 'meal_type', 'notes'
        ]
        read_only_fields = ['meal_id']

    def create(self, validated_data):
        # Remove extra fields that are not part of the model.
        predefined_meal = validated_data.pop('predefined_meal', None)
        validated_data.pop('meal_type', None)
        
        validated_data['user'] = self.context['request'].user
        
        if predefined_meal:
            validated_data['meal_name'] = predefined_meal.fooddescription
            validated_data.setdefault('calories', 0)
            validated_data.setdefault('protein', 0)
            validated_data.setdefault('carbs', 0)
            validated_data.setdefault('fats', 0)
        
        return super().create(validated_data)
