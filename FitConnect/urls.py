from django.urls import path
from .views import *

urlpatterns = [
    path('fitConnect/create_user', CreateUserView.as_view(), name='create-user'),
    path('fitConnect/login', LoginView.as_view(), name='login'),
    path('fitConnect/api', CalorieLogList.as_view()),
    path('fitConnect/api/<int:pk>/', CalorieLogDetails.as_view())
]
