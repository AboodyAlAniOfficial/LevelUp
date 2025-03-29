from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.log_meal, name='log_meal'),
    path('search/', views.search_foods, name='search_foods')
]