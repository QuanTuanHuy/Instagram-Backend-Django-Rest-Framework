from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404, get_list_or_404

from account.models import Profile
from account.serializers import ProfileSerializer

from comment.models import Comment
from comment.serializers import CommentCreateSerializer, CommentSerializer, \
                                CommentDeleteSerializer

from .models import Post, Like, SavedPost, HashTag
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from django.utils.text import slugify

#POSTVIEW
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            owner = Profile.objects.get(user=request.user)

            hashtags = serializer.validated_data.pop('hashtags', [])
            hashtag_objs = set()
            for hashtag in hashtags:
                hashtag = hashtag.lower()
                obj, created = HashTag.objects.get_or_create(name=hashtag)
                hashtag_objs.add(obj)
            
            location = serializer.validated_data.pop('location', None)
            location_obj = None
            if location is not None:
                location_obj, created = Place.objects.get_or_create(name=location,
                                                                    slug=slugify(location))

            post = Post.objects.create(owner=owner, **serializer.validated_data)
            post.hashtags.set(hashtag_objs)
            post.location = location_obj
            post.save()
            return Response(PostSerializer(post).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = self.get_object()
            post.caption = serializer.validated_data['caption']
            post.save()
            return Response(PostSerializer(post).data,
                            status=status.HTTP_202_ACCEPTED)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return PostUpdateSerializer
        return PostSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_post(request):
    owner = Profile.objects.get(user=request.user)
    serializer = PostSerializer(owner.posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_saved(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if profile.profile_name != request.data['profile_name']:
            return Response({"profile_name": "Wrong profile_name"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = SavedPostCreatedSerializer(data=request.data)

        if serializer.is_valid():
            saved_post = serializer.save()
            return Response(SavedPostSerializer(saved_post).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        post_saved = SavedPost.objects.filter(profile=profile)
        serializers = SavedPostSerializer(post_saved, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
        

#what are profile liked this post
@api_view(['GET'])
def profile_liked(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    profile_ids = Like.objects.filter(post=post).select_related('profile') \
                                                .values_list('profile', flat=True)
    profiles = Profile.objects.filter(pk__in=profile_ids)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#LIKE VIEW

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_create(request):
    profile = Profile.objects.get(user = request.user)
    request.data['profile_name'] = profile.profile_name
    serializer = LikeCreateSerializer(data=request.data)

    if serializer.is_valid():
        like = serializer.save()
        return Response(LikeSerializer(like).data ,status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_likes(request):
    profile = get_object_or_404(Profile, user=request.user)
    post_ids = Like.objects.filter(profile=profile).select_related('post') \
                                                .values_list('post', flat=True)
    posts = Post.objects.filter(pk__in=post_ids)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#CommetView

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request):
    profile = Profile.objects.get(user=request.user)
    if profile.profile_name != request.data['profile_name']:
        return Response({"profile_name": "Wrong profile_name"},status=status.HTTP_400_BAD_REQUEST)
    serializer = CommentCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    profile = Profile.objects.get(user=request.user)
    serializer = CommentDeleteSerializer(data=request.data)
    if serializer.is_valid():
        post = get_object_or_404(Post, pk=serializer.validated_data['post_id'])
        comment = get_object_or_404(Comment, pk=serializer.validated_data['comment_id'],
                                    post=post)
        #only owner of comment or owner of post can delete comment
        if post.owner == profile or comment.owner == profile:
            comment.delete()
            return Response({"message": "Delete successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        else: return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_comments(request):
    profile = Profile.objects.get(user=request.user)
    comments = profile.comments
    serializers = CommentSerializer(comments, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])    
def comments_in_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    serializers = CommentSerializer(comments, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)



#NEWS FEED
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def news_feed(request, profile_name):
    profile = get_object_or_404(Profile, profile_name=profile_name,
                                user=request.user)
    followings = profile.me_follow_other.values_list('follow_to', flat=True)
    posts = Post.objects.filter(owner__in=followings)
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

#EXPLORE
@api_view(['GET'])
def post_with_tag(request, tag_name):
    hashtag = get_object_or_404(HashTag, name=tag_name)
    posts = hashtag.posts.all()[:20] or []
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_in_location(request, id, name):
    location = get_object_or_404(Place, pk=id, slug=name)
    posts = location.posts_in_location.all()[:20] or None
    serializers = PostSerializer(posts, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

