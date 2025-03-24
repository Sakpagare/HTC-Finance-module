from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    comp_name = models.CharField(max_length=100)
    comp_logo = models.ImageField(upload_to='logo/')

    def __str__(self):
        return self.username