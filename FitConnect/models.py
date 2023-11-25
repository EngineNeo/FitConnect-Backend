# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class CalorieLog(models.Model):
    calorie_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    amount = models.PositiveIntegerField()
    recorded_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(CalorieLog, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'calorie_log'


class Coach(models.Model):
    coach_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    goal = models.ForeignKey('GoalBank', models.DO_NOTHING, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(Coach, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'coach'


class EquipmentBank(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(EquipmentBank, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'equipment_bank'


class ExerciseBank(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    muscle_group = models.ForeignKey('MuscleGroupBank', models.DO_NOTHING, blank=True, null=True)
    equipment = models.ForeignKey(EquipmentBank, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseBank, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'exercise_bank'


class ExerciseInWorkoutPlan(models.Model):
    exercise_in_plan_id = models.AutoField(primary_key=True)
    plan = models.ForeignKey('WorkoutPlan', models.DO_NOTHING)
    exercise = models.ForeignKey(ExerciseBank, models.DO_NOTHING)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseInWorkoutPlan, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'exercise_in_workout_plan'


class GoalBank(models.Model):
    goal_id = models.AutoField(primary_key=True)
    goal_name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.goal_name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(GoalBank, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'goal_bank'


class MentalHealthLog(models.Model):
    mental_health_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    mood = models.CharField(max_length=7)
    recorded_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MentalHealthLog, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'mental_health_log'


class MessageLog(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('User', models.DO_NOTHING)
    recipient = models.ForeignKey('User', models.DO_NOTHING, related_name='messagelog_recipient_set')
    message_text = models.TextField()
    sent_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MessageLog, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'message_log'


class MuscleGroupBank(models.Model):
    muscle_group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MuscleGroupBank, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'muscle_group_bank'


class PhysicalHealthLog(models.Model):
    physical_health_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    recorded_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(PhysicalHealthLog, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'physical_health_log'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=254)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    goal = models.ForeignKey(GoalBank, models.DO_NOTHING, blank=True, null=True)
    has_coach = models.BooleanField(default=False)
    hired_coach = models.ForeignKey(Coach, models.DO_NOTHING, blank=True, null=True, related_name='user_hired_coach')
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(User, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'user'


class UserCredentials(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    hashed_password = models.CharField(max_length=120)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(UserCredentials, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'user_credentials'


class WaterLog(models.Model):
    water_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    amount = models.IntegerField()
    recorded_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(WaterLog, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'water_log'


class WorkoutLog(models.Model):
    workout_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    exercise_in_plan = models.ForeignKey(ExerciseInWorkoutPlan, models.DO_NOTHING)
    reps = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    completed_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(WorkoutLog, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'workout_log'


class WorkoutPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    plan_name = models.CharField(max_length=255)
    creation_date = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(WorkoutPlan, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'workout_plan'

#Create a custom subclass of DRF Token to work with our custom User class
#From https://stackoverflow.com/questions/66642029/django-rest-framework-generate-a-token-for-a-non-built-in-user-model-class
class AuthToken(Token):
    user = models.OneToOneField(
            User,
            related_name='auth_token',
            on_delete=models.CASCADE,
            verbose_name=gettext_lazy("User")
    )
    class Meta(Token.Meta):
        db_table = 'token'

#Automatically create token when user is created
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        AuthToken.objects.create(user=instance)
