from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Followers
from django.db import connection
from django.db.models import F, Value, ExpressionWrapper
from django.db.models.fields import IntegerField
from daily_goals.models import daily_goals
@api_view(["GET"])
def searchUsers(request):
    query = request.GET.get("q", "")
    print(f"Query received: {query}")  # Debugging log
    users = User.objects.filter(username__icontains=query)
    print(f"Users found: {users}")  # Debugging log
    return JsonResponse({"users": [{"id": u.id, "username": u.username} for u in users]})

@api_view(["POST"])
def followUser(request):
    # Retrieve the usernames of the follower and the user to follow
    follower_username = request.data.get("follower_username")  # The username of the follower
    username_to_follow = request.data.get("username_to_follow")  # The username of the user to be followed

    # Validate input
    if not follower_username or not username_to_follow:
        return JsonResponse({"error": "Both follower and username to follow are required."}, status=400)

    # Ensure the user to follow exists
    user_to_follow = get_object_or_404(User, username=username_to_follow)

    # Prevent self-follow
    if follower_username == username_to_follow:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    # If the follower is an anonymous user, use a specific "anonymous" identifier
    if follower_username == "anonymous":
        follower = None  # Or you can create a placeholder "anonymous" user if needed
    else:
        # Use the username of the follower to retrieve the User object
        follower = get_object_or_404(User, username=follower_username)

    # Check if the follower is already following the user
    if Followers.objects.filter(user_id=follower, following_id=user_to_follow).exists():
        return JsonResponse({"error": f"You are already following {user_to_follow.username}."}, status=400)

    # Create or update the follow relationship
    Followers.objects.get_or_create(user_id=follower, following_id=user_to_follow)
    print(f"Follower: {follower}, User to follow: {user_to_follow}")
    print(f"Checking if already following...")
    return JsonResponse({"message": f"{follower_username} is now following {user_to_follow.username}"}, status=200)



@api_view(["POST"])
def unfollowUser(request):
    follower_username = request.data.get("follower_username")
    username_to_unfollow = request.data.get("username_to_unfollow")
    
    if not follower_username or not username_to_unfollow:
        return JsonResponse({"error": "Both follower and username to unfollow are required."}, status=400)

    user_to_unfollow = get_object_or_404(User, username=username_to_unfollow)
    follower = get_object_or_404(User, username=follower_username)

    # Remove the follow relationship
    followRelationship = Followers.objects.filter(user_id=follower, following_id=user_to_unfollow)
    
    if not followRelationship.exists():
        return JsonResponse({"error": "You are not following this user."}, status=400)

    followRelationship.delete()

    return JsonResponse({"message": f"You have unfollowed {user_to_unfollow.username}"})

#global


@api_view(["GET"])
def getLeaderboard(request):
    leaderboard_data = []

    # Query all users
    users = User.objects.all()

    for user in users:
        health_goal = daily_goals.objects.filter(user=user).values_list('daily_steps_goal', flat=True)
        score = health_goal[0] * 7 if health_goal else 0  # Handle empty or missing goals

        leaderboard_data.append({
            'user': user.username,
            'score': score  
        })

    # Sort the leaderboard by score in descending order
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

    # Add ranking information
    for index, entry in enumerate(leaderboard_data):
        entry['rank'] = index + 1

    return JsonResponse(leaderboard_data, safe=False)



# Function to get user ID based on username
def getuserid(request):
    username = request.GET.get('username')  # Get the 'username' from query parameters
    if not username:
        return JsonResponse({"error": "Username is required"}, status=400)

    # Try to fetch the user based on the username
    user = get_object_or_404(User, username=username)  
    return JsonResponse({"id": user.id}) 

#follower
# PLeaderboard (Followed users only)
@api_view(["GET"])
def getPLeaderboard(request):
    current_user_username = request.GET.get("username")  # Correct query parameter retrieval
    
    if not current_user_username:
        print("No username provided in request.")
        return JsonResponse({"error": "username parameter is required."}, status=400)

    try:
        current_user = User.objects.get(username=current_user_username)
        print(f"Current User Found: {current_user.username}")
    except User.DoesNotExist:
        print(f"User with username '{current_user_username}' does not exist.")
        return JsonResponse({"error": f"User '{current_user_username}' does not exist."}, status=404)

    # Retrieve followed users' IDs
    followed_users_ids = Followers.objects.filter(user_id=current_user).values_list('following_id', flat=True)
    print(f"Followed Users IDs: {followed_users_ids}")

    # Check if there are no followed users
    if not followed_users_ids:
        print("No followed users found.")
        return JsonResponse([], safe=False)

    # Retrieve User objects for followed users
    followed_users = User.objects.filter(id__in=followed_users_ids)
    print(f"Followed Users: {[user.username for user in followed_users]}")

    fleaderboard_data = []
    health_goal = daily_goals.objects.filter(user=current_user).values_list('daily_steps_goal', flat=True)
    score = health_goal[0] * 7 if health_goal else 0
    fleaderboard_data.append({
        'user': current_user.username,
        'score': score
    })
    for follower in followed_users:
        health_goal = daily_goals.objects.filter(user=follower).values_list('daily_steps_goal', flat=True)
        score = health_goal[0] * 7 if health_goal else 0
        print(f"Follower: {follower.username}, Score: {score}")

        fleaderboard_data.append({
            'user': follower.username,
            'score': score
        })

    fleaderboard_data.sort(key=lambda x: x['score'], reverse=True)

    for index, entry in enumerate(fleaderboard_data):
        entry['rank'] = index + 1

    print(f"Final Leaderboard Data: {fleaderboard_data}")
    return JsonResponse(fleaderboard_data, safe=False)


    