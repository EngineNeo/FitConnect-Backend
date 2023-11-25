from django.urls import path
from .views import *

urlpatterns = [
    path('fitConnect/create_user', CreateUserView.as_view(), name='create-user'),
    path('fitConnect/login', LoginView.as_view(), name='login'),
    path('fitConnect/coaches', CoachList.as_view(), name='coach'),
    path('fitConnect/coaches/<int:pk>/', CoachDetail.as_view()),
]
