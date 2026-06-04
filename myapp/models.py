from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Price_Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    medinc = models.CharField(max_length=50)
    houseage = models.CharField(max_length=50)
    averooms = models.CharField(max_length=50)
    avebedrms = models.CharField(max_length=50)
    population = models.CharField(max_length=50)
    aveoccup = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    res = models.CharField(max_length=50)

class UserProfile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(
        upload_to='profile_pics/',  # photos yahan save hongi
        default='profile_pics/default.png',  # default photo
        blank=True,
        null=True
    )
    def __str__(self):
        return self.user.username