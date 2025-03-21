from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Unit, Preferences, HealthData

DEFAULT_PRIVACY = "private"

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
    prefs = Preferences(user=user, privacy=DEFAULT_PRIVACY)
    prefs.save()
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

@api_view(['GET', 'POST'])
def privacy(request: Request) -> Response:
    if request.method == "GET":
        username = request.query_params.get('username')
        return _getprivacy(username)
    elif request.method == "POST":
        username = request.data.get('username')
        setting = request.data.get('setting')
        return _setprivacy(username, setting)

def _getprivacy(username: str) -> Response:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User not found.", status=404)

    prefs_entries = Preferences.objects.filter(user=user)
    if not prefs_entries.exists():
        return Response(DEFAULT_PRIVACY)

    return Response(prefs_entries.first().privacy)

def _setprivacy(username: str, setting: str) -> Response:
    if not setting:
        return Response("No setting provided.")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User not found.", status=404)

    prefs_entries = Preferences.objects.filter(user=user)
    if prefs_entries.exists():
        prefs_entry = prefs_entries.first()
    else:
        prefs_entry = Preferences(user=user)

    prefs_entry.privacy = setting
    prefs_entry.save()
    return Response("Successfully set user’s privacy setting.")

@api_view(['GET', 'POST'])
def healthdata(request: Request) -> Response:
    if request.method == "GET":
        username = request.query_params.get('username')
        field = request.query_params.get('field')
        return _gethealthdata(username, field)
    elif request.method == "POST":
        username = request.data.get('username')
        field = request.data.get('field')
        value = request.data.get('value')
        return _sethealthdata(username, field, value)

def _gethealthdata(username: str, field: str) -> Response:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User not found.", status=404)

    hd_entries = HealthData.objects.filter(user=user)
    if not hd_entries.exists():
        return Response("No health data set for this user.", status=400)

    hd_entry = hd_entries.first()
    if field == "height":
        return Response(hd_entry.height_m)
    elif field == "mass":
        return Response(hd_entry.mass_kg)
    elif field == "age":
        return Response(hd_entry.age_yr)
    elif field == "sex":
        return Response(hd_entry.sex)
    return Response("Invalid field.", status=400)

def _sethealthdata(username: str, field: str, value: float | str) -> Response:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("User not found.", status=404)

    hd_entries = HealthData.objects.filter(user=user)
    if hd_entries.exists():
        hd_entry = hd_entries.first()
    else:
        hd_entry = HealthData(user=user)

    if field == "height":
        hd_entry.height_m = value
    elif field == "mass":
        hd_entry.mass_kg = value
    elif field == "age":
        hd_entry.age_yr = value
    elif field == "sex":
        hd_entry.sex = value
    else:
        return Response("Invalid field.", status=400)

    hd_entry.save()
    return Response("Health data successfully set.")
