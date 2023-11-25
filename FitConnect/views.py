from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from .serializers import *
#from .serializers import UserSerializer, UserCredentialsSerializer
from .models import User, UserCredentials, Coach

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


class CalorieLogList(generics.ListCreateAPIView):
    queryset = CalorieLog.objects.all()
    serializer_class = CalorieLogSerializer


class CalorieLogDetails(generics.RetrieveDestroyAPIView):
    queryset = CalorieLog.objects.all()
    serializer_class = CalorieLogSerializer
        

class WaterLogList(generics.ListCreateAPIView):
    queryset = WaterLog.objects.all()
    serializer_class = WaterLogSerializer


class WaterLogDetails(generics.RetrieveDestroyAPIView):
    queryset = WaterLog.objects.all()
    serializer_class = WaterLogSerializer
    
