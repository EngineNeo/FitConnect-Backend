from rest_framework import status
from rest_framework.generics import get_object_or_404
from ..serializers import PhysicalHealthLogSerializer
from ..models import User

# We would always want our user to log physical health data
# Do we want users to  have to specify AT LEAST one (height, weight)? If so, how to handle?
# Checks:
# If user exists
# Serializer validity
# Outputs:
# If user does not exist or serializer is invalid, function will return response data
# If eligible, function will return None, None (View(s) will do a negative check)


def add_physical_health_log(user_id, weight, height):
    get_object_or_404(User, user_id=user_id)  # Check if user exists
    data = {'user': user_id, 'weight': weight, 'height': height}
    serializer = PhysicalHealthLogSerializer(data=data)
    if serializer.is_valid():  # Check if serializer is valid
        serializer.save()
        return None, None
    else:
        return {"error": "Serializer Error"}, status.HTTP_400_BAD_REQUEST
