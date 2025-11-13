from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_creator = models.BooleanField(default=False)

class Photo(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    people_present = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.title

class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.photo.title}'

class Rating(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        # Each user can only rate a photo once
        unique_together = ('photo', 'user')

    def __str__(self):
        return f'Rating of {self.score} by {self.user.username} on {self.photo.title}'