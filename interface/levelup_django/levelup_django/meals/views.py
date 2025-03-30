from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import LoggedMeal, FoodItem, PredefinedDatabase
from rest_framework import status

@api_view(['GET'])
def index(request):
    return Response("This is the meals index.")

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

@api_view(['POST'])
def log_meal(request):
    print("Incoming POST to /log_meal/")
    print("Raw Request Data:", request.data)

    username = request.data.get('username')
    if not username:
        print("No username provided.")
        return Response({'success': False, 'message': 'Username is required.'}, status=400)

    try:
        user = User.objects.get(username=username)
        print(f"Found user: {user.username} (ID: {user.id})")
    except User.DoesNotExist:
        print(f"User not found: {username}")
        return Response({'success': False, 'message': 'User not found.'}, status=404)

    food_items_data = request.data.get('foods', [])
    if not food_items_data:
        print("No food items provided.")
        return Response({'success': False, 'message': 'No food items provided.'}, status=400)

    print(f"Food items received: {len(food_items_data)}")

    try:
        total_calories = sum(float(item.get('calories', 0)) for item in food_items_data)
        total_protein = sum(float(item.get('protein', 0)) for item in food_items_data)
        total_carbs = sum(float(item.get('carbs', 0)) for item in food_items_data)
        total_fats = sum(float(item.get('fats', 0)) for item in food_items_data)

        print("Totals — Calories:", total_calories,
              "Protein:", total_protein,
              "Carbs:", total_carbs,
              "Fats:", total_fats)

        meal = LoggedMeal.objects.create(
            user=user,
            meal_name=request.data.get('meal_name', 'Untitled Meal'),
            calories=total_calories,
            protein=total_protein,
            carbs=total_carbs,
            fats=total_fats,
            description=request.data.get('description', '')
        )
        print(f"LoggedMeal created with ID {meal.id}")

        for food in food_items_data:
            FoodItem.objects.create(
                meal=meal,
                food_name=food.get('food_name'),
                calories=food.get('calories'),
                protein=food.get('protein'),
                carbs=food.get('carbs'),
                fats=food.get('fats')
            )

        print("Meal and all food items saved successfully.")
        return Response({'success': True, 'message': 'Meal logged with multiple food items.'}, status=201)

    except Exception as e:
        print("Error while logging meal:", str(e))
        import traceback
        traceback.print_exc()
        return Response({'success': False, 'message': str(e)}, status=500)

@api_view(['GET'])
def get_user_meals(request):
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

@api_view(['DELETE'])
def delete_meal(request, meal_id):
    try:
        meal = LoggedMeal.objects.get(id=meal_id)
        meal.delete()
        return Response({"success": True, "message": "Meal deleted successfully."})
    except LoggedMeal.DoesNotExist:
        return Response({"success": False, "message": "Meal not found."}, status=404)

@api_view(['PUT'])
def update_meal(request, meal_id):
    print("UPDATE REQUEST DATA:", request.data)
    try:
        meal = LoggedMeal.objects.get(id=meal_id)
    except LoggedMeal.DoesNotExist:
        return Response({"success": False, "message": "Meal not found."}, status=404)

    food_items_data = request.data.get('foods', [])
    if not food_items_data:
        return Response({'success': False, 'message': 'No food items provided.'}, status=400)

    try:
        meal.meal_name = request.data.get('meal_name', meal.meal_name)
        meal.description = request.data.get('description', meal.description)
        meal.calories = sum(float(item.get('calories', 0)) for item in food_items_data)
        meal.protein = sum(float(item.get('protein', 0)) for item in food_items_data)
        meal.carbs = sum(float(item.get('carbs', 0)) for item in food_items_data)
        meal.fats = sum(float(item.get('fats', 0)) for item in food_items_data)
        meal.save()

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
        print("UPDATE ERROR:", str(e)) 
        return Response({"success": False, "message": str(e)}, status=500)
