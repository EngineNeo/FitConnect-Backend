from rest_framework.generics import get_object_or_404
from ..models import User, PhysicalHealthLog
from rest_framework import status

# We wouldn't want a user to submit an initial survey if they already submitted it
# Checks:
# If user exists
# If goal was already set in user table
# If physical health logs were already entered in physical health log table
# Outputs:
# If user is ineligible or does not exist, function will return response data
# If eligible, function will return None, None (View(s) will do a negative check)


def check_initial_survey_eligibility(user_id):
    get_object_or_404(User, user_id=user_id)  # Check if user exists
    user_has_goal = User.objects.filter(user_id=user_id, goal_id__isnull=False).exists()  # Check if goal already set
    has_physical_health_logs = PhysicalHealthLog.objects.filter(user=user_id).exists()  # Check if p.health log(s) exist
    if user_has_goal and has_physical_health_logs:
        return {"error": "User goal & physical health log(s) already set"}, status.HTTP_400_BAD_REQUEST
    elif user_has_goal:
        return {"error": "User goal already set"}, status.HTTP_400_BAD_REQUEST
    elif has_physical_health_logs:
        return {"error": "User physical health log(s) already exist"}, status.HTTP_400_BAD_REQUEST

    print("User is eligible for initial survey")
    return None, None
