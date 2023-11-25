from rest_framework import serializers
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import User, UserCredentials, Coach, GoalBank

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        validators=[EmailValidator(message='Enter a valid email address')],
    )
    goal = serializers.StringRelatedField(many=False)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'goal', 'has_coach', 'hired_coach']

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)  # exclude the current user when looking
        if queryset.exists():
            raise ValidationError('This email address is already in use.')
        return value

    def validate_hired_coach(self, value):
        if self.instance and self.instance.has_coach:
            if value is None:
                raise ValidationError('User must have a hired coach if has_coach is True')
        return value

class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ['user','hashed_password']

class CoachSerializer(serializers.ModelSerializer):
    goal = serializers.StringRelatedField(many=False)
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    gender = serializers.CharField(read_only=True, source='user.gender')

    # age = today.date() - user.birth_date - ((today.month, today.day) < (birth.month, birth.day))
    class Meta:
        model = Coach
        fields = ['coach_id', 'user_id', 'goal', 'bio', 'cost', 'experience', 'first_name', 'last_name', 'gender'] 

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalBank
        fields = ['goal_id', 'goal_name']
