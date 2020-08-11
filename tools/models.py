from django.db import models
from users.models import CustomUser

class Log(models.Model):
    log	= models.CharField(max_length=512, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    context	= models.CharField(max_length=32, null=False) 
    severity = models.SmallIntegerField() 
    time = models.DateTimeField(blank=True, null = True)
