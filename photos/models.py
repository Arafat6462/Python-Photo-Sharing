from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_creator = models.BooleanField(default=False)

class Photo(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.title