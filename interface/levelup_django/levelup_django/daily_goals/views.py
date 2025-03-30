from django.shortcuts import render
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Daily_GoalsSerializer
from .serializers import calorieSerializer, mealSerializer, dictionarySerializer, stepGoalSerializer, weightGoalSerializer, userSerializer
from .models import daily_goals
from meals.models import LoggedMeal
from accounts.models import User, Unit, Preferences
from django.db import connection
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# Create your views here.
#test view
@api_view(['GET'])
def get_api_urls(request):
    api_urls = {
        'goalList' : '/goalList/'
    }
    
    return Response(api_urls)
@api_view(['GET'])
def search_meal_list(request):
    query = request.query_params.get('q', '')
    results = LoggedMeal.objects.filter(meal_name__icontains=query)[:10]
    meal_names = [item.meal_name for item in results]
    return Response(meal_names)

@api_view(['GET'])
def search_logged_meals(request):
    query = request.GET.get('q', '')
    username = request.GET.get('user', '')

    if not username:
        return Response({'error': 'Username is required'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    meals = LoggedMeal.objects.filter(user=user, meal_name__icontains=query).order_by('-created_at')[:10]
    results = [
        {
            'meal_name': meal.meal_name,
            'calories': meal.calories,
            'id': meal.id,
            'created_at': meal.created_at
        } for meal in meals
    ]
    return Response(results)


@api_view(['POST'])
def createDailyGoals(request):
    try:
        userVal = request.data.get('user_id', None)
        if userVal is not None:
            if not User.objects.filter(id=userVal).exists():
                return Response({"error":"user does not exist"}, status=404)

            daily, created = daily_goals.objects.get_or_create(
                user_id = userVal
            )

            if created:
                return Response({"status":"success", "daily goals created for user_id": userVal}, status=200)
            else:
                return Response({"status":"success", "daily goals already exists for user_id": userVal}, status=200)
            
    except Exception as e:
        return Response({"error":str(e)}, status=500)

@api_view(['GET'])
def get_user_id(request):
    user_name = request.GET.get('username', None)
    if user_name is not None:
        try:
            userVal = User.objects.get(username=user_name)
            user_id = userVal.pk
            serializer = userSerializer(userVal, many=False)
            return Response({"status": "success", "data":serializer.data}, status=200)
        except User.DoesNotExist:
            return Response({"error":"user not found"}, status=404) 
    else:
        return Response({"error":"username not found"}, status=404) 

@api_view(['GET'])
def goalList(request):
    goals = daily_goals.objects.all()
    if goals.exists():
        serializer = Daily_GoalsSerializer(goals, many=True)
        return Response({"status":"success", "data":serializer.data}, status=200)
    else:
        return Response({"error":"goals not found"}, status=404) 

@api_view(['GET'])
def getCalories(request, pk):
    calorieAmount = get_object_or_404(daily_goals, user=pk)
    serializer = calorieSerializer(calorieAmount, many=False)
    return Response({"status":"success", "data":serializer.data}, status=200)

@api_view(['POST'])
def weightGoal(request, pk):
    try:
        weight = request.data.get('weight', None)
        weight = str(weight)
        if weight is None:
            return Response({"error": "Wieght was not provided"}, status=400)
        reg = r'^\d{1,5}(\.\d{1,2})?$'
        if not re.match(reg, weight):
            raise ValidationError("The decimal value exceeds the allowed precision of 5,2")
        decimal_val = Decimal(weight)
        target = daily_goals.objects.get(user=pk)
        target.target_weight = decimal_val
        target.save()
        return Response({"status": "success", "weight": str(decimal_val)}, status=200)
    except InvalidOperation:
        return Response({"error": "Invalid decimal format"}, status=400)
    except ValidationError as e:
        return Response({"error": str(e)},status=400)
    except daily_goals.DoesNotExist:
        return Response({"error":"user does not exist"}, status=404)

@api_view(['POST'])
def stepsGoal(request, pk):
    try:
        steps = request.data.get('steps', None)
        if steps is None:
            return Response({"error": "Steps was not provided"}, status=400)
        steps = int(steps)
        if steps <0:
            return Response({"error": "Steps cannot be negative"}, status=400)
        target = daily_goals.objects.get(user=pk)
        target.daily_steps_goal = steps
        target.save()
        return Response({"status": "success", "steps goal": steps}, status=200)
    except ValueError:
        return Response({"error": "Invalid Integer value"}, status=400)
    except daily_goals.DoesNotExist:
        return Response({"error":"user does not exist"}, status=404)

@api_view(['POST'])
def calculateCalories(request, pk):
    try:
        breakfast = request.data.get('breakfast', None)
        lunch = request.data.get('lunch', None)
        dinner = request.data.get('dinner', None)
        if not (breakfast or lunch or dinner):
            return Response({"error": "no meal was provided"}, status=400)
        meals_data = {}
        calories = 0
        target = LoggedMeal.objects.filter(user=pk)
        for meal_time, name in {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner}.items():
            if name:
                meal_data = target.get(meal_name=name)
                if meal_data:
                    meal = mealSerializer(meal_data)
                    meals_data[meal_time] = meal.data
                    calories += meal_data.calories
                else: 
                    return Response({"error": "meal was not found"}, status=404)
        serializer = dictionarySerializer(data=meals_data)
        if serializer.is_valid():
            return Response({"status": "success", "dailyCalories": calories, "meals data": serializer.data}, status=200)
        return Response({"error": "Invalid serializer"}, status=400)
    except LoggedMeal.DoesNotExist:
        return Response({"error":"an error has occured while trying to calculate calories"}, status=404)

@api_view(['GET'])
def getDailySteps(request, pk):
    stepsAmount = get_object_or_404(daily_goals, user=pk)
    serializer = stepGoalSerializer(stepsAmount, many=False)
    return Response({"status": "success", "steps":serializer.data}, status=200)

@api_view(['GET'])
def getWeightGoal(request, pk):
    currentGoal = get_object_or_404(daily_goals, user=pk)
    serializer = weightGoalSerializer(currentGoal, many=False)
    return Response({"status": "success", "Target":serializer.data}, status=200)

@api_view(['POST'])
def updateDailyCalories(request, pk):
    try:
        calorie = request.data.get("calories", None)
        if calorie is None:
            return Response({"error": "todays calories were not provided"}, status=400)
        calorie = int(calorie)
        target = daily_goals.objects.get(user=pk)
        target.daily_calorie_goal = calorie
        target.save()
        return Response({"status":"success", "daily calorie goal": calorie}, status=200)
    except daily_goals.DoesNotExist:
        return Response({"error": "user does not exist"}, status=404)