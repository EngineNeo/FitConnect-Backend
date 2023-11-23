from rest_framework import status
from ..serializers import PhysicalHealthLogSerializer


def add_physical_health_log(user_id, weight, height):
    data = {'user': user_id, 'weight': weight, 'height': height}
    serializer = PhysicalHealthLogSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer.instance, status.HTTP_201_CREATED
    else:
        return serializer.errors, status.HTTP_400_BAD_REQUEST
