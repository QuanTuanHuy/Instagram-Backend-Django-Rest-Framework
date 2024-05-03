from django.db import models
from django.contrib.auth.models import User

from account.models import Profile
from location.models import Place

class HashTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    owner = models.ForeignKey(Profile, related_name='posts',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='post_pics/', blank=False)
    image = models.URLField(blank=False)
    caption = models.TextField(blank=None)
    location = models.ForeignKey(Place, related_name='posts_in_location',
                                 on_delete=models.SET_NULL,
                                 null=True)
    hashtags = models.ManyToManyField(HashTag, related_name='posts')


    class Meta:
        ordering = ['-created']


class SavedPost(models.Model):
    profile = models.ForeignKey(Profile, related_name='posts_saved',
                                on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='saved_post',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Like(models.Model):
    profile = models.ForeignKey(Profile, related_name='post_liked',
                                on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
