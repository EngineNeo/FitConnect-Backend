from django.urls import path
from .views import *

urlpatterns = [
    path('fitConnect/create_user', CreateUserView.as_view(), name='create-user'),
    path('fitConnect/login', LoginView.as_view(), name='login'),
    
    # These endpoint names are placeholders
    path('fitConnect/calorie_log', CalorieLogList.as_view()),
    path('fitConnect/calorie_log/<int:pk>/', CalorieLogDetails.as_view()),
    path('fitConnect/water_log', WaterLogList.as_view()),
    path('fitConnect/water_log/<int:pk>/', WaterLogDetails.as_view())
]
