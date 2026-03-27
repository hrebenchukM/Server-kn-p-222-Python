from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    birthdate = models.DateField(null=True)