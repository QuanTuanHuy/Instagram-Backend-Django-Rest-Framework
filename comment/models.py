from django.db import models

from account.models import Profile
from post.models import Post

class Comment(models.Model):
    owner = models.ForeignKey(Profile, related_name='comments',
                              on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']
