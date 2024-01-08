from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)
    
    def authenticate(self, request, email=None, password=None, **extra_fields):
        try:
            user = self.get(email=email)
        except self.model.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None


def user_profile_picture_path(instance, filename):
    return f'user_profiles/{instance.id}/{filename}'

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=64, unique=True)
    number_phone = models.CharField(max_length=10, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    description = models.TextField(max_length=200, null=True)
