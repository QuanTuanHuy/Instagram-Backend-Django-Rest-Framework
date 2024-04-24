from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

class Post(models.Model):
    owner = models.ForeignKey(User, related_name="posts",
                              on_delete=models.CASCADE)
    datetime_added = models.DateField(auto_now_add=True)
    image = models.ImageField()
    caption = models.TextField()