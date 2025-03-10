# meals/urls.py

from django.urls import path
from .views import log_meal, daily_calories

urlpatterns = [
    path('log_meal/', log_meal, name='log_meal'),
    path('daily_calories/', daily_calories, name='daily_calories'),
]
