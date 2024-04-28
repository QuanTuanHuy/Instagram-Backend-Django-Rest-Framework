from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404, get_list_or_404

from account.models import Profile
from account.serializers import ProfileSerializer

from comment.serializers import CommentCreateSerializer, CommentSerializer

from .models import Post
from .serializers import *
from .permissions import IsOwnerOrReadOnly

#POSTVIEW
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            owner = Profile.objects.get(user=request.user)
            post = Post.objects.create(owner=owner, **serializer.validated_data)
            post.save()
            return Response(PostSerializer(post).data,
                            status=status.HTTP_201_CREATED)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_comments(request):
    profile = Profile.objects.get(user=request.user)
    comments = profile.comments
    serializers = CommentSerializer(comments, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
    

    