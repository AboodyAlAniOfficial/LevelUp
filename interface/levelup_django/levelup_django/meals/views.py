from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import PredefinedMeal, LoggedMeal
from .serializers import PredefinedMealSerializer, LoggedMealSerializer

@api_view(['GET'])
def search_predefined_meals(request):
    """
    GET /api/v1/meals/search/?q=<term>
    Searches 'fooddata' by 'fooddescription__icontains'
    """
    query = request.query_params.get('q', '')
    if query:
        items = PredefinedMeal.objects.filter(fooddescription__icontains=query)
    else:
        items = PredefinedMeal.objects.none()
    serializer = PredefinedMealSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_logged_meal(request):
    """
    POST /api/v1/meals/create/
    Expects JSON like:
    {
      "meal_name": "Pizza Pepperoni",
      "calories": 300,
      "protein": 15,
      "carbs": 30,
      "fats": 10,
      "description": "Custom user note..."
    }
    """
    # We attach the user to the data so the row in 'meals' references user_id
    data = request.data.copy()
    
    # Explicitly set user_id
    data['user'] = request.user.id
    
    serializer = LoggedMealSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error saving meal: {str(e)}")
            return Response({"detail": f"Error saving meal: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    print(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)