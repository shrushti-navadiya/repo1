from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.is_staff:
            return True
        return False

    def has_module_perms(self, app_label):
        if app_label == 'admin':
            return True
        return False

class Exam(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exams", limit_choices_to={'role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)

class Answer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)

class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    status = models.CharField(max_length=10, choices=[('pass', 'Pass'), ('fail', 'Fail')])
