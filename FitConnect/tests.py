from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from .models import User, Coach, CalorieLog, WaterLog, PhysicalHealthLog, MentalHealthLog, GoalBank, MuscleGroupBank, ExerciseBank, EquipmentBank
from .views import WorkoutPlanList, DailySurveyView, InitialSurveyView, SearchExercises


# RUNNING TESTS AND GENERATING htmlcov SUBDIRECTORY:
# Command to run coverage for testing (put the name of your virtual environment inside the --omit='*/<your VE name>/*'):
# coverage run --omit='*/.venv/*' manage.py test

# To generate coverage report, run the command:
# coverage html

# The first command generates the information that the second command creates the report from
# The coverage report can be found in ./htmlcov/index.html

# Test Endpoints
class TestCreateUserEndpoint(TestCase):
    def setUp(self):
        # Create a user for testing
        self.username = 'testuser'
        self.user = User.objects.create(first_name=self.username)

    def test_user_exists(self):
        # Check if the user exists in the database
        user_exists = User.objects.filter(user_id=1).exists()
        self.assertTrue(user_exists, f"User '{self.username}' does not exist.")


class TestWorkoutPlanListEndpoint(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'wTestUser'
        self.user = User.objects.create(first_name=self.username)

    def test_workout_plan_list_view(self):
        request = self.factory.get('/fitConnect/plan')
        response = WorkoutPlanList.as_view()(request)
        self.assertEquals(response.status_code, 200)


class TestDailySurveyEndpoint(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Set Test Recorded Date
        recorded_date = '2023-12-10'

        # Create Test User
        self.user_f_name = 'Test'
        self.user_l_name = 'User'
        self.test_user = User.objects.create(first_name=self.user_f_name, last_name=self.user_l_name)

        # Create Calorie Log
        self.cal_amount = 100
        self.calorie_log = CalorieLog.objects.create(user=self.test_user, amount=self.cal_amount, recorded_date=recorded_date)

        # Create Water Log
        self.water_amount = 50
        self.water_log = WaterLog.objects.create(user=self.test_user, amount=self.water_amount, recorded_date=recorded_date)

        # Create Mental Health Log
        self.mood = 'Happy'
        self.mental_health_log = MentalHealthLog.objects.create(user=self.test_user, mood=self.mood, recorded_date=recorded_date)

        # Create Physical Health Log
        self.weight = 150.0
        self.physical_health_log = PhysicalHealthLog.objects.create(user=self.test_user, weight=self.weight, recorded_date=recorded_date)


    def test_daily_survey_view_get(self):
        # Assert Get Response returns 200
        request = self.factory.get('/fitConnect/daily_survey/')
        response = DailySurveyView.as_view()(request, user_id=self.test_user.user_id)
        self.assertEquals(response.status_code, 200)

        # Assert Response for invalid user_id is 400
        response = DailySurveyView.as_view()(request, user_id=2)
        self.assertEquals(response.status_code, 400)

    
    def test_daily_survey_view_post(self):
        # Assert Post request response is 201
        request = self.factory.post('/fitConnect/daily_survey/', {"recorded_date": "2023-12-10", "calorie_amount": 1000, "water_amount": 500, "mood": "Sad", "weight": 150.0})
        response = DailySurveyView.as_view()(request, user_id=self.test_user.user_id)
        self.assertEquals(response.status_code, 201)

        # Assert Post request for invalid user is 400
        response = DailySurveyView.as_view()(request, user_id=2)
        self.assertEquals(response.status_code, 400)


class TestInitialSurveyEndpoint(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create Test User
        self.user_f_name = 'Test'
        self.user_l_name = 'User'
        self.test_user = User.objects.create(first_name=self.user_f_name, last_name=self.user_l_name)

        # Create a Test Goal
        self.goal_name = 'Lose Weight'
        self.goal = GoalBank.objects.create(goal_name=self.goal_name)

    def test_initial_survey_view_post(self):
        request = self.factory.post('/fitConnect/initial_survey', {"user_id": self.test_user.user_id, "goal_id": self.goal.goal_id, "weight": 150.0, "height": 75.0})
        response = InitialSurveyView.as_view()(request)
        self.assertEquals(response.status_code, 201)


class TestSearchExercisesEndpoint(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create Test Muscle Group
        self.muscle_name = 'Biceps'
        self.muscle_group = MuscleGroupBank.objects.create(name=self.muscle_name)

        # Create Test Equipment
        self.equipment_name = 'Flat Bench'
        self.equipment = EquipmentBank.objects.create(name=self.equipment_name)

        # Create Test Exercise
        self.exercise_name = 'Bench Press'
        self.exercise = ExerciseBank.objects.create(name=self.exercise_name, muscle_group=self.muscle_group, equipment=self.equipment)

    def test_exercise_search_view(self):
        request = self.factory.get('/fitConnect/exercises/search/', {"exercise_id": self.exercise.exercise_id, "muscle_group_id": self.muscle_group.muscle_group_id, "equipment_id": self.equipment.equipment_id})
        response = SearchExercises.as_view()(request)
        self.assertEquals(response.status_code, 200)
    
    
