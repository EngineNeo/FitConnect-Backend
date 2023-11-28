from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .serializers import UserSerializer, UserCredentialsSerializer
from .models import User, UserCredentials, Coach
from .services.physical_health import add_physical_health_log
from .services.goals import update_user_goal
from .services.initial_survey_eligibility import check_initial_survey_eligibility
import django


def validate_password(password):
    if len(password) < 7:
        raise ValidationError("Password must be 7 characters or more.")

    hasSpecialChar = not password.isalnum()
    hasNum = any(char.isdigit() for char in password)
    hasLetter = any(char.isalpha() for char in password)

    if not hasSpecialChar or not hasNum or not hasLetter:
        raise ValidationError("Password must contain at least one number, letter, and special character")

class CreateUserView(APIView):
    def post(self, request, format=None):
        password = request.data.pop("password")
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                validate_password(password)
            except ValidationError as err:
                print('password was invalid')
                return Response(err, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            ph = PasswordHasher()
            hashed_password = ph.hash(password)
            credentials_serializer = UserCredentialsSerializer(data={'user' : serializer.data['user_id'],'hashed_password' : hashed_password})

            if credentials_serializer.is_valid():
                credentials_serializer.save()
            else:
                print('Credential serialization went wrong somehow')
                return Response(credentials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print('serializer was not valid')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def check_password(self, user_id, password): #Checks that provided password matches the stored hash
        ph = PasswordHasher()
        user_credentials = UserCredentials.objects.get(pk=user_id)
        hash = getattr(user_credentials, 'hashed_password')
        try:
            ph.verify(hash,password)
            return True
        except VerifyMismatchError as e:
            return False

    def get(self, request):
        email = request.query_params.get("email")
        try:
            django.core.validators.validate_email(email) #Check that email is valid before hitting db
            user = User.objects.get(email=email)         #Will throw exception if user does not exist
        except:
            return Response({'Error' : 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = getattr(user, 'user_id')
        password = request.query_params.get("password")

        if self.check_password(user_id, password): #Verify that the password was correct
            user_serializer = UserSerializer(user)
            response={'token' : user.auth_token.key}
            if Coach.objects.filter(user_id=user_id).exists(): #Get user type by checking if user_id exists in the coach table
                user_type = 'coach'
            else:
                user_type = 'user'
            response.update({'user_type' : user_type})
            response.update(user_serializer.data)
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response({'Error' : 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)


# Requirements:
# All fields filled, user goal is null, user has no physical health logs
class InitialSurveyView(APIView):
    def post(self, request):
        # Extract data from the request
        user_id = request.data.get('user_id')
        goal_id = request.data.get('goal_id')
        weight = request.data.get('weight')
        height = request.data.get('height')
        # Initial Survey requires all fields
        if not all([user_id, goal_id, weight, height]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        # Call survey eligibility function
        eligibility_response, eligibility_status = check_initial_survey_eligibility(user_id)
        # Check if eligible for survey
        if eligibility_response is not None:
            return Response(eligibility_response, eligibility_status)
        # Call update user goal function
        update_goal_response, update_goal_status = update_user_goal(user_id, goal_id)
        # Check if goal update failed
        if update_goal_response is not None:
            return Response(update_goal_response, update_goal_status)
        # Call add physical health log function
        physical_health_response, physical_health_status = add_physical_health_log(user_id, weight, height)
        # Check if add physical health log failed
        if physical_health_response is not None:
            # Might want to reset goal to null (previous value)
            update_user_goal(user_id, None)
            return Response(physical_health_response, status=physical_health_status)
        # Return the response
        return Response({"success": "Survey completed successfully"}, status=status.HTTP_201_CREATED)
