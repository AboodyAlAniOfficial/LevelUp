import json

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# TEMP don't require csrf
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Unit
# Create your views here.

def index(request):
    return HttpResponse("This is the accounts index.")

@csrf_exempt
def register(request):
    if User.objects.filter(username=request.POST['username']):
        return HttpResponse(json.dumps({ 'success': False }))

    user = User.objects.create_user(
        request.POST['username'], password=request.POST['password'])
    return HttpResponse(json.dumps({ 'success': True }))

@csrf_exempt
def login(request):
    user = authenticate(username=request.POST['username'],
                        password=request.POST['password'])
    data = { 'success': user is not None }
    if user is not None:
        data['username'] = request.POST['username']
    return HttpResponse(json.dumps(data))

@csrf_exempt
def unit(request) -> HttpResponse:
    if request.method == "GET":
        return _getunit(
            username=request.GET['username'],
            dimension=request.GET['dimension'])
    elif request.method == "POST":
        return _setunit(
            username=request.POST['username'],
            dimension=request.POST['dimension'],
            unitname=request.POST['unitname'])

def _getunit(username: str, dimension: str) -> HttpResponse:
    user = User.objects.get(username=username)
    units_entries = Unit.objects.filter(user=user)
    if units_entries:
        units_entry = units_entries.first()
    else:
        return HttpResponse("No units set for this user.")

    if dimension == "length":
        return HttpResponse(units_entry.length)
    elif dimension == "mass":
        return HttpResponse(units_entry.mass)
    elif dimension == "energy":
        return HttpResponse(units_entry.energy)

def _setunit(username: str, dimension: str, unitname: str) -> HttpResponse:
    user = User.objects.get(username=username)
    units_entries = Unit.objects.filter(user=user)
    if units_entries:
        units_entry = units_entries.first()
    else:
        units_entry = Unit(user=user)

    if dimension == "length":
        units_entry.length = unitname
        units_entry.save()
    elif dimension == "mass":
        units_entry.mass = unitname
        units_entry.save()
    elif dimension == "energy":
        units_entry.energy = unitname
        units_entry.save()
    else:
        raise ValueError("Unidentified dimension.")
    return HttpResponse("Unit successfully set.")
