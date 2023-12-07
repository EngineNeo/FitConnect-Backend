import datetime
from rest_framework import serializers
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import User, UserCredentials, Coach, GoalBank, PhysicalHealthLog, BecomeCoachRequest, WorkoutPlan, ExerciseInWorkoutPlan, ExerciseBank


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        validators=[EmailValidator(message='Enter a valid email address')],
    )
    goal = serializers.StringRelatedField(many=False)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'goal', 'has_coach',
                  'hired_coach', 'created', 'last_update']

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)  # exclude the current user when looking
        if queryset.exists():
            raise ValidationError('This email address is already in use.')
        return value

    def validate_hired_coach(self, value):
        if self.instance and self.instance.has_coach:
            if value is None and self.initial_data['has_coach'] != False:
                raise ValidationError('User must have a hired coach if has_coach is True')
        return value


class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ['user', 'hashed_password']


class CoachSerializer(serializers.ModelSerializer):
    goal = serializers.StringRelatedField(many=False)
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    gender = serializers.CharField(read_only=True, source='user.gender')

    class Meta:
        model = Coach
        fields = ['coach_id', 'user_id', 'goal', 'bio', 'cost', 'experience', 'first_name', 'last_name', 'gender']

    def validate_cost(self, value):
        if value < 0:
            raise ValidationError('Cost cannot be negative.')
        return value

    def validate_experience(self, value):
        if value < 0:
            raise ValidationError('Experience cannot be negative.')
        return value


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalBank
        fields = ['goal_id', 'goal_name']


class CoachRequestSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    coach = serializers.IntegerField()

    def save(self):
        user_instance = User.objects.get(pk=self.validated_data['user'])
        user_instance.has_coach = False
        user_instance.hired_coach = Coach.objects.get(pk=self.validated_data['coach'])
        user_instance.save()

    def validate_user(self, value):
        try:
            user_instance = User.objects.get(pk=value)
        except User.DoesNotExist:
            print('User does not exist.')
            raise ValidationError('User does not exist.')
        if user_instance.has_coach:
            print('User already has a coach.')
            raise ValidationError('User already has a coach.')

        if user_instance.hired_coach is not None:
            print('User has already requested a coach.')
            raise ValidationError('User has already requested a coach.')
        return value

    def validate_coach(self, value):
        if not Coach.objects.filter(pk=value).exists():
            print('Coach does not exist.')
            raise ValidationError('Requested coach does not exist.')
        return value


class CoachAcceptSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    coach = serializers.IntegerField()

    def save(self):
        user_instance = User.objects.get(pk=self.validated_data['user'])
        user_instance.has_coach = True
        user_instance.hired_coach = Coach.objects.get(pk=self.validated_data['coach'])
        user_instance.save()

    def validate_user(self, value):
        try:
            user_instance = User.objects.get(pk=value)
        except User.DoesNotExist:
            print('User does not exist.')
            raise ValidationError('User does not exist.')

        if user_instance.has_coach:
            print('User already has a coach.')
            raise ValidationError('User already has a coach.')

        return value

    def validate_coach(self, value):
        if not Coach.objects.filter(pk=value).exists():
            print('Coach does not exist.')
            raise ValidationError('Coach does not exist.')

        try:
            user_instance = User.objects.get(pk=self.initial_data['user'])
        except User.DoesNotExist:
            user_instance = None

        if user_instance is not None and user_instance.hired_coach_id != value:
            print('Coach was not requested by user.')
            raise ValidationError('User has not requested this coach.')

        return value


class PhysicalHealthLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalHealthLog
        fields = '__all__'


class BecomeCoachRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BecomeCoachRequest
        fields = '__all__'
    # Django auto checks if user exists, goal exists, and user did not already submit a 'become coach' request
    def validate_experience(self, experience):
        if experience < 0:
            raise serializers.ValidationError('experience can not be negative')
        return experience

    def validate_cost(self, cost):
        if cost < 0:
            raise serializers.ValidationError('cost can not be negative')
        return cost

class ExerciseSerializer(serializers.ModelSerializer):
    muscle_group_name = serializers.CharField(source='muscle_group.name', read_only=True)
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)

    class Meta:
        model = ExerciseBank
        fields = ['exercise_id', 'name', 'description', 'muscle_group_name', 'equipment_name']


class ExerciseInWorkoutPlanSerializer(serializers.ModelSerializer):
    class RelatedExerciseField(serializers.PrimaryKeyRelatedField):
        """
        Allows ExerciseInWorkoutPlanSerializer to take an exercise_id for the exercise instead of an instance. 
        """
        def to_representation(self, value):
            value = super().to_representation(value)
            exercise = self.queryset.get(pk=value)
            return ExerciseSerializer(exercise).data

    exercise = RelatedExerciseField(queryset=ExerciseBank.objects.all())

    class Meta:
        model = ExerciseInWorkoutPlan
        fields = ['exercise_in_plan_id', 'plan_id', 'exercise', 'sets', 'reps', 'weight', 'duration_minutes']

    def validate_plan_id(self, value):
        if not WorkoutPlan.objects.filter(pk=value).exists():
            raise ValidationError('Plan does not exist')
        else:
            return value

    def create(self, validated_data):
        plan_id = validated_data.pop('plan_id')
        plan = WorkoutPlan.objects.get(pk=plan_id)
        return ExerciseInWorkoutPlan.objects.create(**validated_data, plan=plan)


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = ExerciseInWorkoutPlanSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['plan_id', 'user_id', 'plan_name', 'creation_date', 'exercises']

    '''
    def update(self, instance, validated_data):
        print("data:", validated_data)
        exercises = validated_data.pop("exercises", None)
        print("exercises:", exercises)

        for exercise in exercises:
            exercise['exercise'] = exercise.pop('exercise_id')

        updated_exercises = [exercise for exercise in exercises if 'exercise_in_plan_id' in exercise]
        for exercise in updated_exercises:
            exercises.remove(exercise)

        exercise_serializer = ExerciseInWorkoutPlanSerializer(data=exercises, many=True)
        if exercise_serializer.is_valid():
            exercise_serializer.save(plan=instance)
        else:
            raise ValidationError(exercise_serializer.errors)

        instance.plan_name = validated_data.get("plan_name", instance.plan_name)
        instance.save()
        return instance
    '''
