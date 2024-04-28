from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE)
    profile_name = models.CharField(unique=True, max_length=30)
    bio = models.CharField(max_length=1000, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
