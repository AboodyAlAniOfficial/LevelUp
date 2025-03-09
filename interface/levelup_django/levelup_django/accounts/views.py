import json

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# TEMP don't require csrf
from django.views.decorators.csrf import csrf_exempt

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

