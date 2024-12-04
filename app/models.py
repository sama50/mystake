from django.db import models

# Create your models here.


class PattiGame(models.Model):
    status = models.CharField(max_length=10,default='OPEN')