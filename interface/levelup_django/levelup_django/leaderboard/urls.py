from django.urls import path
from .views import getPLeaderboard, getLeaderboard, searchUsers, unfollowUser, followUser, getuserid


app_name = 'leaderboard'
urlpatterns = [
    path('search/', searchUsers, name='search-users'),

    path('follow/', followUser, name='follow-user'),
    path('unfollow/', unfollowUser, name='unfollow-user'),
    path('getuserid/', getuserid, name='get-user-id'), 
    path('global/', getLeaderboard, name='global-leaderboard'),
    path('fleaderboard/', getPLeaderboard, name='followed-leaderboard'),
]
