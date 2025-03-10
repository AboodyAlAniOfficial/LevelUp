from django.contrib import admin
from .models import FoodItem, Nutrient, FoodNutrientAmount

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('food_id', 'description', 'scientific_name')
    search_fields = ('description', 'scientific_name')

@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    list_display = ('nutrient_id', 'name', 'unit')
    search_fields = ('name', 'symbol')

@admin.register(FoodNutrientAmount)
class FoodNutrientAmountAdmin(admin.ModelAdmin):
    list_display = ('food', 'nutrient', 'nutrient_value')
    search_fields = ('food__description', 'nutrient__name')

# Now, these models will appear in the Django admin panel
