from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("unit/", views.unit, name="unit"),
    path("privacy/", views.privacy, name="privacy"),
    path("healthdata/", views.healthdata, name="healthdata"),
    path("bmr/", views.bmr, name="bmr"),
]
