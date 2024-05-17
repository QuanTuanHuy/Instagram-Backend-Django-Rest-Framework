from rest_framework import serializers

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from location.models import Place
from account.models import Profile

from .models import Post, Like, SavedPost

#HASHTAG
class HashTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

#POST
class PostCreateSerializer(serializers.Serializer):
    image = serializers.URLField(required=True)
    caption = serializers.CharField()
    location = serializers.CharField(required=False)
    #list of hashtags
    hashtags = serializers.ListField(child=serializers.CharField() ,required=False)

class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='pk')
    class Meta:
        model = Post
        fields = ['id' ,'profile_name', 'image', 'caption', 'created', 'hashtags', 'location']
        read_only_fields = ['id' ,'profile_name', 'image', 'created', 'location', 'hashtags']
        depth = 1
    
    def get_profile_name(self, obj):
        return obj.owner.profile_name
    
    def get_location(self, obj):
        if obj.location is None:
            return []
        return (obj.location.pk, obj.location.name)
    

class PostUpdateSerializer(serializers.Serializer):
    caption = serializers.CharField()

class SavedPostSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    savedAt = serializers.DateTimeField(source='created')
    class Meta:
        model = SavedPost
        fields = ['profile_name', 'post', 'savedAt']
        depth = 1
    
    def get_profile_name(self, obj):
        return obj.profile.profile_name

class SavedPostCreatedSerializer(serializers.Serializer):
    profile_name = serializers.CharField()
    post_id = serializers.IntegerField()

    # def validate_post_id(self, value):
    #     post = get_object_or_404(Post, pk=value)
    #     return value

    def create(self, validated_data):
        profile = get_object_or_404(Profile, profile_name=validated_data['profile_name'])
        post = get_object_or_404(Post, pk=validated_data['post_id'])

        try:
            saved_post = SavedPost.objects.get(profile=profile, post=post)
            saved_post.delete()
            return saved_post
        except:
            pass 
        saved_post = SavedPost.objects.create(profile=profile, post=post)
        saved_post.save()
        return saved_post


#LIKE
class LikeSerializer(serializers.ModelSerializer):
    profile_name = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['profile_name', 'post_id', 'created']

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
            post.number_of_likes -= 1
            post.save()
            return like
        except Like.DoesNotExist:
            like = Like.objects.create(profile=profile, post=post)
            like.save()
            post.number_of_likes += 1
            return like