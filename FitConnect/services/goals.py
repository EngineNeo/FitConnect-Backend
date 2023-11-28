from rest_framework.generics import get_object_or_404
from ..models import User, GoalBank
from rest_framework import status
from ..serializers import UserSerializer

# We wouldn't want a user to update goal if the specified goal_id does not exist
# Checks:
# If user DNE
# If goal DNE
# Serializer validity
# Outputs:
# If user or goal DNE, or serializer is invalid, function will return response data
# If user exists & goal exists, function will return None, None (View(s) will do a negative check)
# Special Case: Goal ID reset to null when initial survey physical health log insertion fails
#               Function will return None, None. Response data is used from physical_health function

def update_user_goal(user_id, goal_id):
    user = get_object_or_404(User, user_id=user_id)  # Check if user exists
    if goal_id is None:  # Special Case
        user.goal_id = None
        user.save()
        return None, None
    if not GoalBank.objects.filter(goal_id=goal_id).exists():  # Check if goal exists
        return {"error": "Invalid goal_id"}, status.HTTP_400_BAD_REQUEST
    user.goal_id = goal_id
    serializer = UserSerializer(user, data={'goal_id': goal_id}, partial=True)
    if serializer.is_valid():  # Check if serializer is valid
        serializer.save()
        return None, None
    else:
        return {"error": "Serializer Error"}, status.HTTP_400_BAD_REQUEST
