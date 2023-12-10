from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from django.views.decorators.csrf import csrf_exempt

from .models import ExerciseInWorkoutPlan, User, UserCredentials, Coach, AuthToken, WorkoutPlan, ExerciseBank, MuscleGroupBank, EquipmentBank, BecomeCoachRequest

from .services.physical_health import add_physical_health_log
from .services.goals import update_user_goal
from .services.initial_survey_eligibility import check_initial_survey_eligibility
from django.utils import timezone
from django.http import JsonResponse, Http404
import django, json

from .serializers import *

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
            credentials_serializer = UserCredentialsSerializer(
                data={'user': serializer.data['user_id'], 'hashed_password': hashed_password})

            if credentials_serializer.is_valid():
                credentials_serializer.save()
            else:
                print('Credential serialization went wrong somehow')
                return Response(credentials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print('serializer was not valid')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def check_password(self, user_id, password):  # Checks that provided password matches the stored hash
        ph = PasswordHasher()
        user_credentials = UserCredentials.objects.get(pk=user_id)
        hash = getattr(user_credentials, 'hashed_password')
        try:
            ph.verify(hash, password)
            return True
        except VerifyMismatchError as e:
            return False

    def post(self, request):
        email = request.data.get("email")
        try:
            django.core.validators.validate_email(email)  # Check that email is valid before hitting db
            user = User.objects.get(email=email)  # Will throw exception if user does not exist
        except:
            return Response({'Error': 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = getattr(user, 'user_id')
        password = request.data.get("password")

        if self.check_password(user_id, password):  # Verify that the password was correct
            user_serializer = UserSerializer(user)

            token, created = AuthToken.objects.get_or_create(user=user)

            response = {'token': token.key, 'user_type': 'user'}

            if Coach.objects.filter(user_id=user_id).exists():
                response['user_type'] = 'coach'

            response.update(user_serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        user = request.data.get('user_id')
        token = get_object_or_404(AuthToken, user__user_id=user)
        token.delete()
        return Response(status=status.HTTP_200_OK)

  
class CoachList(APIView):
    def validate_search_params(self, params):
        # Validate query. Maybe make this a serializer later idk
        goal = params.get('goal')

        experience = params.get('experience')
        if experience is not None:
            experience = int(experience)
            print('experience=', experience)
            if experience < 0:
                raise ValidationError('Experience cannot be negative')

        cost = params.get('cost')
        if cost is not None:
            cost = float(cost)
            if cost < 0:
                raise ValidationError('Cost cannot be negative')

        return [goal, experience, cost]

    def get(self, request):
        try:
            goal, min_experience, cost = self.validate_search_params(request.query_params)
        except ValidationError as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        # If search criteria is passed, filter the queryset
        # Consider allowing filtering for multiple goals; max and min cost; max and min experience
        coaches = Coach.objects.all()
        if cost is not None:
            coaches = coaches.filter(cost__lte=cost)
        if goal is not None:
            coaches = coaches.filter(goal__goal_id=goal)
        if min_experience is not None:
            coaches = coaches.filter(experience__gte=min_experience)

        serializer = CoachSerializer(coaches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CoachDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class RequestCoach(APIView):
    def patch(self, request):
        # expecting {'user' : user_id, 'coach' : coach_id}
        request = CoachRequestSerializer(data=request.data)
        if request.is_valid():
            request.save()
            return Response('Requested coach successfully', status=status.HTTP_200_OK)
        else:
            return Response(request.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptClient(APIView):
    def patch(self, request):
        # expecting {'user' : user_id, 'coach' : coach_id}
        request = CoachAcceptSerializer(data=request.data)
        if request.is_valid():
            request.save()
            return Response('Accepted client successfully', status=status.HTTP_200_OK)
        else:
            return Response(request.errors, status=status.HTTP_400_BAD_REQUEST)


class FireCoach(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return None

    def patch(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response("User does not exist.", status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializer(user, data={'has_coach' : False, 'hired_coach' : None}, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response('Successfully fired coach.', status=status.HTTP_200_OK)
        else:
            print('Invalid:', user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachClients(APIView):
    hired = None

    def get(self, request, pk):
        clients = User.objects.filter(has_coach=self.hired, hired_coach__coach_id=pk)
        clients_serializer = UserSerializer(clients, many=True)
        return Response(clients_serializer.data, status=status.HTTP_200_OK)


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


# Requirements
# All fields filled, user exists, goal exists, user did not already request to become coach, cost & exp are not negative
class BecomeCoachRequestView(APIView):  # This is the coach initial survey
    def post(self, request):
        serializer = BecomeCoachRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Coach initial survey completed successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Will return each error


class ManageBecomeCoachRequestView(APIView):
    # Example Accept
    # { "user_id": 12, "is_approved": true }
    # Example Deny
    # { "user_id": 14 }
    # List all coach requests that have is_approved set to null
    def get(self, request):
        coach_requests = BecomeCoachRequest.objects.filter(is_approved__isnull=True)
        serializer = ViewBecomeCoachRequestSerializer(coach_requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        coach_request = self.get_object_by_user_id(user_id)

        if not coach_request:
            return Response({"error": "BecomeCoachRequest does not exist for the specified user."},
                            status=status.HTTP_400_BAD_REQUEST)

        is_approved = request.data.get('is_approved')
        if is_approved:
            coach_data = {
                'user': user_id,
                'experience': coach_request.experience,
                'cost': coach_request.cost,
                'goal': coach_request.goal.pk,
                'bio': coach_request.bio,
            }
            coach_serializer = DomCoachSerializer(data=coach_data)
            if coach_serializer.is_valid():
                coach_serializer.save()
                coach_request.is_approved = True
                coach_request.save()
                return Response({"success": "Coach request approved and Coach created successfully."},
                                status=status.HTTP_201_CREATED)
            return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            coach_request.is_approved = False
            coach_request.save()
            return Response({"success": "Coach request denied successfully."}, status=status.HTTP_200_OK)

    def get_object_by_user_id(self, user_id):
        try:
            return BecomeCoachRequest.objects.get(user=user_id, is_approved__isnull=True)
        except BecomeCoachRequest.DoesNotExist:
            return None


class EditExerciseBankView(APIView):
    # Example add exercise
    # { "name": "Sick Exercise","description": "Hey there!","muscle_group": 1, "equipment": 1 }
    def post(self, request, *args, **kwargs):
        serializer = DomExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Example deactivate exercise
    # {"exercise_id": 1}
    def put(self, request):
        exercise_id = request.data.get('exercise_id')
        try:
            exercise = ExerciseBank.objects.get(exercise_id=exercise_id)
        except ExerciseBank.DoesNotExist:
            return Response({"detail": "Exercise not found."}, status=status.HTTP_404_NOT_FOUND)
        exercise.is_active = False
        exercise.save()
        return Response({"detail": "Exercise disabled successfully."}, status=status.HTTP_200_OK)

@csrf_exempt
def create_workout_plan(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        # find the workout plan data
        user_id = data.get('user')
        plan_name = data.get('planName')
        creation_date = data.get('creationDate')

        # create workout plan
        workout_plan = WorkoutPlan.objects.create(
            user_id=user_id,
            plan_name=plan_name,
            creation_date=creation_date,
            created=timezone.now(),
            last_update=timezone.now()
        )

        # find exercise data
        exercises_data = json.loads(data.get('exercises'))

        # Create ExerciseInWorkoutPlan objects
        for exercise_data in exercises_data:
            ExerciseInWorkoutPlan.objects.create(
                plan=workout_plan,
                exercise_id=exercise_data.get('exercise'),
                sets=exercise_data.get('sets'),
                reps=exercise_data.get('reps'),
                weight=exercise_data.get('weight'),
                duration_minutes=exercise_data.get('durationMinutes'),
                created=timezone.now(),
                last_update=timezone.now()
            )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class WorkoutPlanList(APIView):
    def get(self, request, user_id=None):
        plans = WorkoutPlan.objects.all()
        plan_name = request.query_params.get("name")
        if user_id is not None:
            plans = plans.filter(user__user_id=user_id)
        if plan_name:
            plans = plans.filter(plan_name__icontains=plan_name)
        serializer = WorkoutPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        return create_workout_plan(request)

class WorkoutPlanDetail(APIView):
    def get(self, request, pk):
        plan = get_object_or_404(WorkoutPlan, pk=pk)
        if plan is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutPlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        plan = get_object_or_404(WorkoutPlan, pk=pk)
        serializer = WorkoutPlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan = get_object_or_404(WorkoutPlan, pk=pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExerciseInWorkoutPlanView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            queryset = ExerciseInWorkoutPlan.objects.all()
            serializer = ExerciseInWorkoutPlanSerializer(queryset, many=True)
        else:
            exercise_in_plan = get_object_or_404(ExerciseInWorkoutPlan, pk=pk)
            serializer = ExerciseInWorkoutPlanSerializer(exercise_in_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        if pk is None:
            pk = request.data.pop('exercise_in_plan_id')
        exercise_in_plan = get_object_or_404(ExerciseInWorkoutPlan, pk=pk)
        serializer = ExerciseInWorkoutPlanSerializer(exercise_in_plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        print('data: ', request.data)
        serializer = ExerciseInWorkoutPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        exercise_in_plan = get_object_or_404(ExerciseInWorkoutPlan, pk=pk)
        exercise_in_plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Visitor View for Exercises
class ExerciseList(generics.ListAPIView):
    queryset = ExerciseBank.objects.filter(is_active=1)
    serializer_class = ExerciseListSerializer

class ExerciseListId(generics.RetrieveAPIView):
    queryset = ExerciseBank.objects.filter(is_active=1)
    serializer_class = ExerciseListSerializer

class MuscleGroupList(generics.ListAPIView):
    queryset = MuscleGroupBank.objects.all()
    serializer_class = MuscleGroupBankSerializer


class EquipmentList(generics.ListAPIView):
    queryset = EquipmentBank.objects.all()
    serializer_class = EquipmentBankSerializer


class SearchExercises(APIView):
    def get(self, request, *args, **kwargs):
        # Get the request parameters
        exercise_id = request.query_params.get('exercise_id')
        muscle_group_id = request.query_params.get('muscle_group_id')
        equipment_id = request.query_params.get('equipment_id')

        queryset = ExerciseBank.objects.filter(is_active=1)

        if exercise_id:
            queryset = queryset.filter(exercise_id=exercise_id)

        if muscle_group_id:
            queryset = queryset.filter(muscle_group__muscle_group_id=muscle_group_id)

        if equipment_id:
            queryset = queryset.filter(equipment__equipment_id=equipment_id)


        serializer = ExerciseSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DailySurveyView(APIView):
    # Sample JSON format for GET and POST requests
    # These are attached to a user_id in the url, for example the following JSON could be posted to the endpoint:
    # /fitConnect/daily_survey/1/

    # {
    #     "recorded_date": "2023-11-29",
    #     "calorie_amount": 1500,
    #     "water_amount": 1000,
    #     "mood": "Happy"
    # }

    # Which would be for the user with user_id=1
    # A GET request will return a list of JSON in the above format

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the last 5 logs for each type
            calorie_logs = CalorieLog.objects.filter(
                user_id=user_id).order_by('-recorded_date')[:5]
            water_logs = WaterLog.objects.filter(
                user_id=user_id).order_by('-recorded_date')[:5]
            mental_health_logs = MentalHealthLog.objects.filter(
                user_id=user_id).order_by('-recorded_date')[:5]
            physical_health_logs = PhysicalHealthLog.objects.filter(
                user_id=user_id).order_by('-recorded_date')[:5]

            data = {}

            # Process calorie logs
            for log in calorie_logs:
                date = log.recorded_date
                if date not in data:
                    data[date] = {'recorded_date': date, 'calorie_amount': None,
                                'water_amount': None, 'mood': None, 'weight': None}
                data[date]['calorie_amount'] = log.amount

            # Process water logs
            for log in water_logs:
                date = log.recorded_date
                if date not in data:
                    data[date] = {'recorded_date': date, 'calorie_amount': None,
                                'water_amount': None, 'mood': None, 'weight': None}
                data[date]['water_amount'] = log.amount

            # Process mental health logs
            for log in mental_health_logs:
                date = log.recorded_date
                if date not in data:
                    data[date] = {'recorded_date': date, 'calorie_amount': None,
                                'water_amount': None, 'mood': None, 'weight': None}
                data[date]['mood'] = log.mood

            # Process physical health logs
            for log in physical_health_logs:
                date = log.recorded_date
                if date not in data:
                    data[date] = {'recorded_date': date, 'calorie_amount': None,
                                'water_amount': None, 'mood': None, 'weight': None}
                data[date]['weight'] = log.weight

            # Return data for the last 5 recorded entries of each type
            return Response(list(data.values()), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    def post(self, request, user_id):
        # Check to see if the requested user exists in the database
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist as e:
            return Response({'error:': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = DailySurveySerializer(data=request.data)
            if serializer.is_valid():
                # This assumes that recorded_date, calorie_amount, water_amount, and mood are all required fields
                recorded_date = serializer.validated_data['recorded_date']
                calorie_amount = serializer.validated_data['calorie_amount']
                water_amount = serializer.validated_data['water_amount']
                mood = serializer.validated_data['mood']
                weight = serializer.validated_data['weight']

                # Save data to respective models
                CalorieLog.objects.create(user_id=user_id, amount=calorie_amount, recorded_date=recorded_date)
                WaterLog.objects.create(user_id=user_id, amount=water_amount, recorded_date=recorded_date)
                MentalHealthLog.objects.create(user_id=user_id, mood=mood, recorded_date=recorded_date)
                PhysicalHealthLog.objects.create(user_id=user_id, weight=weight, recorded_date=recorded_date)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
