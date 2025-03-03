from django.urls import path
from . import views


urlpatterns = [
    path('meals/', views.meals, name='meals'),
]