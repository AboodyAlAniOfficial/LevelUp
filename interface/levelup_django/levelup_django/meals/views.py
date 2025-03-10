from rest_framework import viewsets
from .models import FoodItem, Nutrient, FoodNutrientAmount
from .serializers import FoodItemSerializer, NutrientSerializer, FoodNutrientAmountSerializer

class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only API
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class NutrientViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only API
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer

class FoodNutrientAmountViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only API
    queryset = FoodNutrientAmount.objects.all()
    serializer_class = FoodNutrientAmountSerializer
