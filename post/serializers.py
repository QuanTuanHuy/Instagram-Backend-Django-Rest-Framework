from rest_framework import serializers

from location.models import Place
from account.models import Profile

from .models import Post

choices = [('', 'No Location')] + list(Place.objects.all())

class PostCreateSerializer(serializers.Serializer):
    image = serializers.ImageField()
    caption = serializers.CharField()
    location = serializers.ChoiceField(choices=choices, required=False)

class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='pk')
    class Meta:
        model = Post
        fields = ['id' ,'profile_name', 'image', 'caption', 'created', 'location']
        read_only_fields = ['id' ,'profile_name', 'image', 'created', 'location']
    
    def get_profile_name(self, obj):
        return obj.owner.profile_name
    
    def get_location(self, obj):
        if obj.location is None:
            return []
        return (obj.location.pk, obj.location.name)
    
class PostUpdateSerializer(serializers.Serializer):
    caption = serializers.CharField()