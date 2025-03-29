from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Follower
from django.db import connection

@api_view(["GET"])
def searchUsers(request):
    query = request.GET.get("q", "")
    users = User.objects.filter(username__icontains=query)[:10]  # Limit results
    return JsonResponse({"users": [{"id": u.id, "username": u.username} for u in users]})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def followUser(request):
    # Get the username from the request data
    username_to_follow = request.data.get("username")
    
    # Retrieve the user object based on the username
    user_to_follow = get_object_or_404(User, username=username_to_follow)
    
    # Prevent users from following themselves
    if user_to_follow == request.user:
        return JsonResponse({"error": "You cannot follow yourself"}, status=400)
    
    # Create a follow relationship
    Follower.objects.get_or_create(follower=request.user, following=user_to_follow)
    
    # Return a success response
    return JsonResponse({"message": f"You are now following {user_to_follow.username}"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollowUser(request):
    user_to_unfollow = get_object_or_404(User, id=request.data.get("user_id"))
    Follower.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return JsonResponse({"message": f"You have unfollowed {user_to_unfollow.username}"})
#global
@api_view(["GET"])
def getLeaderboard(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.username,
                COALESCE(SUM(e.duration_minutes) * 100, 0) AS score
            FROM levelup.Users u
            LEFT JOIN levelup.Exercises e ON u.user_id = e.user_id
            GROUP BY u.user_id, u.username
            ORDER BY score DESC;
        """)
        
        leaderboard_data = cursor.fetchall()

    leaderboard_result = [
        {idx + 1, row[0], row[1]}
        for idx, row in enumerate(leaderboard_data)
    ]

    return JsonResponse({"leaderboard": leaderboard_result})
#follower
@api_view(["GET"])
def getFollowedLeaderboard(request):
    current_user_id = request.user.id  

    with connection.cursor() as cursor:
        cursor.execute("""
            WITH FollowedUsers AS (
                SELECT follows_user_id AS followed_id 
                FROM levelup.Followers 
                WHERE user_id = %s
            )
            SELECT 
                u.username,
                COALESCE(SUM(e.duration_minutes) * 100, 0) AS score
            FROM levelup.Users u
            JOIN FollowedUsers f ON u.user_id = f.followed_id
            LEFT JOIN levelup.Exercises e ON u.user_id = e.user_id
            GROUP BY u.user_id, u.username
            ORDER BY score DESC;
        """, [current_user_id])
        
        leaderboard_data = cursor.fetchall()

    # Format response with Rank, Username, Score
    leaderboard_result = [
        {idx + 1, row[0], row[1]}
        for idx, row in enumerate(leaderboard_data)
    ]

    return JsonResponse({"leaderboard": leaderboard_result})