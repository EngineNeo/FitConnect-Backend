from rest_framework.generics import get_object_or_404

from ..models import User, PhysicalHealthLog
from rest_framework import status
from rest_framework.response import Response

def check_initial_survey_eligibility(user_id):
    user = get_object_or_404(User, user_id=user_id) # If user id DNE, 404.
    user = User.objects.filter(user_id=user_id, goal_id__isnull=False).first()
    if user:
        return Response({"error": "User already has a goal set"}, status=status.HTTP_400_BAD_REQUEST)
    if PhysicalHealthLog.objects.filter(user=user_id).exists():
        return Response({"error": "User already has physical health log(s)"}, status=status.HTTP_400_BAD_REQUEST)
    return None