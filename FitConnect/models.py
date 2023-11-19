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


class Coach(models.Model):
    coach_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    category = models.ForeignKey('CoachCategory', models.DO_NOTHING, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    state = models.ForeignKey('State', models.DO_NOTHING)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.user)
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(Coach, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'coach'


class CoachCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.category_name
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(CoachCategory, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'coach_category'


class CoachReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(Coach, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    review_date = models.DateField()
    def __str__(self):
        return self.user
    class Meta:
        managed = False
        db_table = 'coach_review'


class EquipmentForExercise(models.Model):
    exercise_equipment_id = models.AutoField(primary_key=True)
    exercise = models.ForeignKey('Exercise', models.DO_NOTHING)
    equipment = models.ForeignKey('ExerciseEquipment', models.DO_NOTHING)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.equipment
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(EquipmentForExercise, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'equipment_for_exercise'


class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('ExerciseCategory', models.DO_NOTHING)
    muscle_group_id = models.PositiveIntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(Exercise, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'exercise'


class ExerciseCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseCategory, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'exercise_category'


class ExerciseEquipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseEquipment, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'exercise_equipment'


class ExerciseInWorkoutPlan(models.Model):
    exercise_in_plan_id = models.AutoField(primary_key=True)
    plan = models.ForeignKey('WorkoutPlan', models.DO_NOTHING)
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    complete_by_date = models.DateField()
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.exercise
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseInWorkoutPlan, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'exercise_in_workout_plan'


class ExerciseMedia(models.Model):
    media_id = models.AutoField(primary_key=True)
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    coach = models.ForeignKey(Coach, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    media_type = models.CharField(max_length=5)
    media_url = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateField()
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseMedia, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'exercise_media'


class ExerciseMuscleCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(ExerciseMuscleCategory, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'exercise_muscle_category'


class FitnessGoal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    exercise = models.ForeignKey(Exercise, models.DO_NOTHING)
    description = models.TextField()
    creation_date = models.DateField()
    date_to_complete = models.DateField()
    achieved = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(FitnessGoal, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'fitness_goal'


class IntakeLog(models.Model):
    intake_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    intake_type = models.CharField(max_length=7)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    def __str__(self):
        return self.user
    class Meta:
        managed = False
        db_table = 'intake_log'


class MentalHealthLog(models.Model):
    health_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    stress_level = models.CharField(max_length=6)
    sleep_quality = models.CharField(max_length=9)
    mood = models.CharField(max_length=7)
    recorded_date = models.DateField()
    def __str__(self):
        return self.user
    class Meta:
        managed = False
        db_table = 'mental_health_log'


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('User', models.DO_NOTHING)
    recipient = models.ForeignKey('User', models.DO_NOTHING, related_name='message_recipient_set')
    message_text = models.TextField()
    sent_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.sender
    class Meta:
        managed = False
        db_table = 'message'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey('Subscription', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(Payment, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'payment'


class PhysicalHealthLog(models.Model):
    health_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    measure_type = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    def __str__(self):
        return self.user
    class Meta:
        managed = False
        db_table = 'physical_health_log'


class ProgressPhoto(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    photo_path = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    def __str__(self):
        return self.user
    class Meta:
        managed = False
        db_table = 'progress_photo'


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.state_name
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(State, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'state'


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey('User', models.DO_NOTHING)
    coach = models.ForeignKey(Coach, models.DO_NOTHING)
    subscription_start_date = models.DateField(blank=True, null=True)
    subscription_end_date = models.DateField(blank=True, null=True)
    isActive = models.IntegerField(db_column='isActive', blank=True, null=True)  
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.subscriber
    class Meta:
        managed = False
        db_table = 'subscription'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=254)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(User, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'user'


class UserCredentials(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    hashed_password = models.CharField(max_length=120)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(UserCredentials, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'user_credentials'


class WeightGoal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    target_weight = models.PositiveIntegerField()
    creation_date = models.DateField()
    date_to_complete = models.DateField()
    achieved = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user
    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(WeightGoal, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'weight_goal'


class WorkoutLog(models.Model):
    workout_id = models.AutoField(primary_key=True)
    plan = models.ForeignKey('WorkoutPlan', models.DO_NOTHING, blank=True, null=True)
    exercise_in_plan = models.ForeignKey(ExerciseInWorkoutPlan, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    coach_id = models.PositiveIntegerField(blank=True, null=True)
    workout_date = models.DateField()
    sets = models.PositiveIntegerField(blank=True, null=True)
    reps = models.PositiveIntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.plan
    class Meta:
        managed = False
        db_table = 'workout_log'


class WorkoutPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    coach = models.ForeignKey(Coach, models.DO_NOTHING, blank=True, null=True)
    plan_name = models.CharField(max_length=255)
    creation_date = models.DateField()
    last_update = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.plan_name
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
