from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.log_meal, name='log_meal'),
    path('search/', views.search_foods, name='search_foods'),
    path('user/', views.get_user_meals, name='get_user_meals'),
    path('<int:meal_id>/delete/', views.delete_meal, name='delete_meal'),
    path('<int:meal_id>/update/', views.update_meal, name='update_meal')
]
