from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .queryFunctions import get_user_id
from .followerModel import Follower

@csrf_exempt  # Ignore the authentication token requirement

# This method implements the logic of how the user is able to follow another user. 
# It relies on a JSON file to read from the JavaScript file that uses Axios.
def followUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')  # ID of the user instance
            followerUsername = data.get('username')  # Username to follow

            # Check if the user exists in the database
            followsUserId = get_user_id(followerUsername)  # Get ID of the account to follow
            if not followsUserId:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Output an error message if the user tries to follow themselves
            if user_id == followsUserId:
                return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

            # Check if the follow relationship already exists
            if Follower.objects.filter(user_id=user_id, followerUserId=followsUserId).exists():
                return JsonResponse({'error': 'Already following this user'}, status=400)

            # Creates a follower relationship using followerModel.py
            Follower.objects.create(user_id=user_id, followerUserId=followsUserId)  
            return JsonResponse({'message': f'User {user_id} is now following {followerUsername}'})  # Output message if successful

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Handle unexpected errors

    return JsonResponse({'error': 'Invalid request'}, status=400)  # Output if following failed


