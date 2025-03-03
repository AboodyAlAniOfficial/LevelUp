from django.shortcuts import render
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Daily_GoalsSerializer
from .serializers import calorieSerializer
from .models import daily_goals
from django.db import connection
from django.shortcuts import get_object_or_404, get_list_or_404


# Create your views here.
#test view
@api_view(['GET'])
def get_api_urls(request):
    api_urls = {
        'goalList' : '/goalList/'
    }
    
    return Response(api_urls)
#return all goals in the database
@api_view(['GET'])
def goalList(request):
    goals = daily_goals.objects.all()
    if goals.exists():

        serializer = Daily_GoalsSerializer(goals, many=True)
        return Response({"status":"success", "data":serializer.data}, status=200)
    else:
        return Response({"error":"goals not found"}, status=404) 

#get the current calories
@api_view(['GET'])
def getCalories(request, pk):
    
    
    calorieAmount = get_object_or_404(daily_goals, user=pk)
    

    serializer = calorieSerializer(calorieAmount, many=False)
    return Response({"status":"success", "data":serializer.data}, status=200)
   
#Set a new target weight fot the user
@api_view(['POST'])
def weightGoal(request, pk):
    
    
    
    try:
        
        weight = request.data.get('weight', None)
        
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

#update the steps goal for the user
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
    return 
