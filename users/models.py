from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)