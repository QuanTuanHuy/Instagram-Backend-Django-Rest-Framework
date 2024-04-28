from rest_framework import serializers

from post.models import Post
from account.models import Profile

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'created', 'content']
        depth = 1

class CommentCreateSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    content = serializers.CharField()
    profile_name = serializers.CharField()

    def validate_post_id(self, value):
        if Post.objects.filter(pk=value).exists():
            return value
        raise serializers.ValidationError("Post does't exists")
    
    def validate_content(self, value):
        if len(value) > 0:
            return value
        raise serializers.ValidationError("Content can't empty")

    def create(self, validated_data):
        profile = Profile.objects.get(profile_name=validated_data['profile_name'])
        post = Post.objects.get(pk=validated_data['post_id'])
        comment = Comment.objects.create(owner=profile, post=post,
                                         content=validated_data['content'])
        comment.save()
        return comment