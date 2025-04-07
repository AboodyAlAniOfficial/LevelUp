from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import LoggedMeal, FoodItem, PredefinedDatabase
from rest_framework import status

@api_view(['GET'])
def index(request):
    return Response("This is the meals index.")

# This function searches for food items in the PredefinedDatabase based on a query parameter
# It returns a list of food items that match the query
@api_view(['GET'])
def search_foods(request):
    query = request.query_params.get('q', '')
    results = PredefinedDatabase.objects.filter(Food__icontains=query)[:10]
    data = [
        {
            "food_id": item.Food_id,
            "food": item.Food,
            "measure": item.Measure,
            "grams": item.Grams,
            "calories": item.Calories,
            "proteins": item.Proteins,
            "fats": item.Fats,
            "carbs": item.Carbs
        }
        for item in results
    ]
    return Response(data)

# This function logs a meal with multiple food items

@api_view(['POST'])
def log_meal(request):
    username = request.data.get('username')
    if not username:
        return Response({'success': False, 'message': 'Username is required.'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User not found.'}, status=404)
    # Check if the user is authenticated
    food_items_data = request.data.get('foods', [])
    if not food_items_data:
        return Response({'success': False, 'message': 'No food items provided.'}, status=400)

    try:
        total_calories = sum(float(item.get('calories', 0)) for item in food_items_data)
        total_protein = sum(float(item.get('protein', 0)) for item in food_items_data)
        total_carbs = sum(float(item.get('carbs', 0)) for item in food_items_data)
        total_fats = sum(float(item.get('fats', 0)) for item in food_items_data)
        # Create a new meal entry in the database
        meal = LoggedMeal.objects.create(
            user=user,
            meal_name=request.data.get('meal_name', 'Untitled Meal'),
            calories=total_calories,
            protein=total_protein,
            carbs=total_carbs,
            fats=total_fats,
            description=request.data.get('description', '')
        )
        # Create food items associated with the meal
        for food in food_items_data:
            FoodItem.objects.create(
                meal=meal,
                food_name=food.get('food_name'),
                calories=food.get('calories'),
                protein=food.get('protein'),
                carbs=food.get('carbs'),
                fats=food.get('fats')
            )

        return Response({'success': True, 'message': 'Meal logged with multiple food items.'}, status=201)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)

# This function retrieves all meals logged by a user
@api_view(['GET'])
def get_user_meals(request):
    # Get the username from the query parameters
    username = request.query_params.get('username')
    if not username:
        return Response({'success': False, 'message': 'Username is required.'}, status=400)

    try:
        user = User.objects.get(username=username)
        meals = LoggedMeal.objects.filter(user=user).order_by('-created_at')
        data = []
        for meal in meals:
            foods = [
                {
                    "food_name": f.food_name,
                    "calories": f.calories,
                    "protein": f.protein,
                    "carbs": f.carbs,
                    "fats": f.fats,
                }
                for f in meal.foods.all()
            ]
            # Append the meal data to the list
            # Include the food items in the response
            data.append({
                "id": meal.id,
                "meal_name": meal.meal_name,
                "description": meal.description,
                "date": meal.created_at.strftime('%Y-%m-%d %H:%M'),
                "foods": foods
            })
        return Response({"meals": data})

    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User not found.'}, status=404)

# This function deletes a meal by its ID
@api_view(['DELETE'])
def delete_meal(request, meal_id):
    try:
        # It takes a meal ID as a URL parameter
        meal = LoggedMeal.objects.get(id=meal_id)
        # and deletes the meal with that ID from the database
        meal.delete()
        return Response({"success": True, "message": "Meal deleted successfully."})
    except LoggedMeal.DoesNotExist:
        return Response({"success": False, "message": "Meal not found."}, status=404)

#  This function updates a meal and its associated food items  
# It takes a meal ID as a URL parameter and expects the updated meal data in the request body
@api_view(['PUT'])
def update_meal(request, meal_id):
    try:
        # Get the meal by ID
        meal = LoggedMeal.objects.get(id=meal_id)
    except LoggedMeal.DoesNotExist:
        return Response({"success": False, "message": "Meal not found."}, status=404)

    food_items_data = request.data.get('foods', [])
    if not food_items_data:
        return Response({'success': False, 'message': 'No food items provided.'}, status=400)

    try:
        # Update the meal details
        meal.meal_name = request.data.get('meal_name', meal.meal_name)
        meal.description = request.data.get('description', meal.description)
        meal.calories = sum(float(item.get('calories', 0)) for item in food_items_data)
        meal.protein = sum(float(item.get('protein', 0)) for item in food_items_data)
        meal.carbs = sum(float(item.get('carbs', 0)) for item in food_items_data)
        meal.fats = sum(float(item.get('fats', 0)) for item in food_items_data)
        meal.save()

        # Update the food items associated with the meal
        # First, delete the existing food items
        meal.foods.all().delete()
        for food in food_items_data:
            FoodItem.objects.create(
                meal=meal,
                food_name=food.get('food_name'),
                calories=food.get('calories'),
                protein=food.get('protein'),
                carbs=food.get('carbs'),
                fats=food.get('fats')
            )

        return Response({"success": True, "message": "Meal updated successfully."})

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)