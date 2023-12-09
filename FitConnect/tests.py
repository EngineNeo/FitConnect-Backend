from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from .models import User, CalorieLog
from .views import CalorieLogList

# Command to run coverage for testing
# coverage run --omit='*/.venv/*' manage.py test

# Test Endpoints
class TestCalorieLogEndpoints(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        request = self.factory.get('/fitConnect/calorie_log')
        response = CalorieLogList.as_view()(request)
        self.assertEqual(response.status_code, 200)


