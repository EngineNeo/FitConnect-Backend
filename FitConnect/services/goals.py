from ..models import User, GoalBank
from rest_framework import status
from ..serializers import UserSerializer

def update_user_goal(user_id, goal_id):
    # Check if the provided goal_id exists in the goal bank
    if not GoalBank.objects.filter(goal_id=goal_id).exists():
        return {"error": "Invalid goal_id"}, status.HTTP_400_BAD_REQUEST
    try:
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user, data={'user_id': user_id, 'goal_id': goal_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return user, status.HTTP_202_ACCEPTED
        else:
            return serializer.errors, status.HTTP_400_BAD_REQUEST

    except User.DoesNotExist:
        return {"error": "User not found"}, status.HTTP_404_NOT_FOUND