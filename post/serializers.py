from rest_framework import serializers

from .models import Post

class PostSerializers(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Post
        fields = ['owner_profile_name', 'created', 'image',
                  'caption', 'location_name']