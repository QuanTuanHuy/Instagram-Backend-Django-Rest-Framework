from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status 

from django.contrib.auth.models import User

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Profile.objects.create(user=user)
        return super().perform_create(serializer)
    
class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        if user != request.user:
            return Response({"message": "You can not update other password"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
class ProfileDetail(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

