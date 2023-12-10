from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from .models import User, CalorieLog
from .views import DailySurveyView


# Command to run coverage for testing
# coverage run --omit='*/.venv/*' manage.py test

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