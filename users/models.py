from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here
    platform = models.CharField(max_length=32, null=True, blank = True) ## Where did I contacted the customer
    other = models.CharField(max_length=64, null = True, blank = True)
    subscription = models.CharField(max_length=32, default = 'free')

    def __str__(self):
        return self.email