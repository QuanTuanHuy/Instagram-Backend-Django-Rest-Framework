from rest_framework import serializers

from location.models import Place
from account.models import Profile

from .models import Post

class PostCreateSerializer(serializers.Serializer):
    image = serializers.ImageField()
    caption = serializers.CharField()
    location = serializers.ChoiceField(choices=Place.objects.all(), required=False)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'