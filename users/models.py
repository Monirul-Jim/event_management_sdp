from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='event_images', blank=True, default='event_images/profilepic.png')
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
