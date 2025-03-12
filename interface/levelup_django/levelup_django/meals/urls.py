from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('search/', views.search_predefined_meals, name='search_predefined_meals'),
    path('create/', views.create_logged_meal, name='create_logged_meal'),
]
