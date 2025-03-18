from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Unit

@api_view(['GET'])
def index(request):
    return Response("This is the accounts index.")

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'success': False, 'message': 'Username already exists.'})
    
    User.objects.create_user(username=username, password=password)
    user = User.objects.get(username=username)
    unit = Unit(user=user, length="m", mass="kg", energy="kJ")
    unit.save()
    return Response({'success': True})

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    data = {'success': user is not None}
    if user:
        data['username'] = username
    return Response(data)

@api_view(['GET', 'POST'])
def unit(request):
    if request.method == "GET":
        username = request.query_params.get('username')
        dimension = request.query_params.get('dimension')
        return _getunit(username, dimension)
    elif request.method == "POST":
        username = request.data.get('username')
        dimension = request.data.get('dimension')
        unitname = request.data.get('unitname')
        return _setunit(username, dimension, unitname)

def _getunit(username, dimension):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User not found.", status=404)
    
    units_entries = Unit.objects.filter(user=user)
    if not units_entries.exists():
        return Response("No units set for this user.", status=404)
    
    units_entry = units_entries.first()
    if dimension == "length":
        return Response(units_entry.length)
    elif dimension == "mass":
        return Response(units_entry.mass)
    elif dimension == "energy":
        return Response(units_entry.energy)
    return Response("Invalid dimension.", status=400)

def _setunit(username, dimension, unitname):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User not found.", status=404)
    
    units_entries = Unit.objects.filter(user=user)
    if units_entries.exists():
        units_entry = units_entries.first()
    else:
        units_entry = Unit(user=user)
    
    if dimension == "length":
        units_entry.length = unitname
    elif dimension == "mass":
        units_entry.mass = unitname
    elif dimension == "energy":
        units_entry.energy = unitname
    else:
        return Response("Invalid dimension.", status=400)
    
    units_entry.save()
    return Response("Unit successfully set.")
