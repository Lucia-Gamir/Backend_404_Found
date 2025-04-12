from django.db import models
from django.contrib.auth.models import AbstractUser 

class CustomUser(AbstractUser): 
    birth_date = models.DateField()
    locality = models.CharField(max_length=100, blank=True)
    municipality = models.CharField(max_length=100, blank=True)
    dni = models.CharField(max_length=10, blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    direction = models.CharField(max_length=255, blank=True)
    payment = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)