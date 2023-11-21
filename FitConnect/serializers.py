from django.db.models import Avg
from rest_framework import serializers
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import User, UserCredentials, Coach, CoachReview

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        validators=[EmailValidator(message='Enter a valid email address')],
    )

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'creation_date', 'last_update']

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)  # exclude the current user when looking
        if queryset.exists():
            raise ValidationError('This email address is already in use.')
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

    class Meta:
        model = Coach
        fields = ['coach_id', 'user_id', 'goal', 'bio', 'first_name', 'last_name', 'gender', 'cost', 'experience'] 

    '''
    def to_representation(self, instance):
        data = super(CoachSerializer, self).to_representation(instance)
        avg_rating = CoachReview.objects.filter(coach_id=instance.coach_id).aggregate(Avg('rating'))['rating__avg'] or 0.0 #Get average reviews, or 0 for no reviews
        data.update({'rating' : avg_rating})
        return data
    '''
