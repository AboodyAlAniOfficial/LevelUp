from django.urls import path
from .views import followed_leaderboard, leaderboard

urlpatterns = [
    path('leaderboard/followed/', followed_leaderboard, name='followed-leaderboard'),
    path('leaderboard/global/', leaderboard, name='global-leaderboard'),
]