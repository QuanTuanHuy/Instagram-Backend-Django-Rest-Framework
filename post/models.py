from django.db import models
from django.contrib.auth.models import User

from account.models import Profile
from location.models import Place

# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(Profile, related_name='posts',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_pics/', blank=False)
    caption = models.TextField(blank=None)
    location = models.ForeignKey(Place, related_name='posts_in_location',
                                 on_delete=models.SET_NULL,
                                 null=True)

