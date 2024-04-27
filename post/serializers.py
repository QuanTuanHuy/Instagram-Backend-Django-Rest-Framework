from rest_framework import serializers

from django.shortcuts import get_object_or_404

from location.models import Place
from account.models import Profile

from .models import Post, Like

choices = [('', 'No Location')] + list(Place.objects.all())

#POST
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


#LIKE
class LikeSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['profile_name', 'post_id', 'created']
        depth = 1

    def get_profile_name(self, obj):
        return obj.profile.profile_name
    
    def get_post_id(self, obj):
        return obj.post.pk
    
class LikeCreateSerializer(serializers.Serializer):
    profile_name = serializers.CharField()
    post_id = serializers.IntegerField()

    def create(self, validated_data):
        profile = Profile.objects.get(profile_name=validated_data['profile_name'])
        post = get_object_or_404(Post, pk=validated_data['post_id'])
        try:
            like = Like.objects.get(profile=profile, post=post)
            like.delete()
            return like
        except:
            pass

        like = Like.objects.create(profile=profile, post=post)
        like.save()
        return like