from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from account.models import Profile

from .models import Post
from .serializers import *
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class PostCreate(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(**serializer.validated_data, owner=profile)
            post.save()
            return Response(PostSerializer(post).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# class PostDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateSerializer
#     permission_classes = [IsOwnerOrReadOnly]