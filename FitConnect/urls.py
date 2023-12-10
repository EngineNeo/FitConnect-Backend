from django.urls import path
from .views import *

urlpatterns = [
    path('fitConnect/create_user', CreateUserView.as_view(), name='create-user'),
    path('fitConnect/login', LoginView.as_view(), name='login'),
    path('fitConnect/coaches', CoachList.as_view(), name='coach'),
    path('fitConnect/coaches/<int:pk>', CoachDetail.as_view()),
    path('fitConnect/coaches/<int:pk>/requests', CoachClients.as_view(hired=False)),
    path('fitConnect/coaches/<int:pk>/clients', CoachClients.as_view(hired=True)),
    path('fitConnect/requestCoach/', RequestCoach.as_view()),
    path('fitConnect/acceptClient/', AcceptClient.as_view()),
    path('fitConnect/fireCoach/<int:pk>', FireCoach.as_view()),
    path('fitConnect/initial_survey', InitialSurveyView.as_view(), name='initial-survey'),
    path('fitConnect/create_workout_plan', create_workout_plan, name='create_workout_plan'),
    path('fitConnect/daily_survey/<int:user_id>/', DailySurveyView.as_view(), name='daily_survey'),

    path('fitConnect/exercises', ExerciseList.as_view()),
    path('fitConnect/exercises/<int:pk>', ExerciseListId.as_view()),
    path('fitConnect/muscle_groups', MuscleGroupList.as_view()),
    path('fitConnect/equipment', EquipmentList.as_view()),
    path('fitConnect/exercises/search/', SearchExercises.as_view()),

    path('fitConnect/become_coach', BecomeCoachRequestView.as_view(), name='become-coach-request'),
    path('fitConnect/users/<int:user_id>/plans', WorkoutPlanList.as_view()),
    path('fitConnect/plans', WorkoutPlanList.as_view()),
    path('fitConnect/plans/<int:pk>', WorkoutPlanDetail.as_view()),
    path('fitConnect/exercise_in_plan/', ExerciseInWorkoutPlanView.as_view()),
    path('fitConnect/exercise_in_plan/<int:pk>', ExerciseInWorkoutPlanView.as_view()),

    path('fitConnect/manage_become_coach_request', ManageBecomeCoachRequestView.as_view()),
    path('fitConnect/edit_exercise_bank', EditExerciseBankView.as_view()),

    path('fitConnect/logout/', LogoutView.as_view(), name='logout'),

    path('fitConnect/create_workout_log/', WorkoutLogCreateView.as_view(), name='create_workout_log'),
]
