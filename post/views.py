from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from account.models import Profile

from .models import Post
from .serializers import *
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            owner = Profile.objects.get(user=request.user)
            post = Post.objects.create(owner=owner, **serializer.validated_data)
            post.save()
            return Response(PostSerializer(post).data,
                            status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = self.get_object()
            post.caption = serializer.validated_data['caption']
            post.save()
            return Response(PostSerializer(post).data,
                            status=HTTP_202_ACCEPTED) 

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ('partial_update', 'update'):
            return PostUpdateSerializer
        return PostSerializer