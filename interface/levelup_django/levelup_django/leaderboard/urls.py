from django.urls import path
from .views import followed_leaderboard, leaderboard


app_name = 'leaderboard'

urlpatterns = [
    path('users/search/', searchUsers, name='search-users'),
    path('users/follow/', followUser, name='follow-user'),
    path('users/unfollow/', unfollowUser, name='unfollow-user'),
    path('leaderboard/global/', getLeaderboard, name='global-leaderboard'),
    path('leaderboard/followed/', getFollowedLeaderboard, name='followed-leaderboard'),
]
