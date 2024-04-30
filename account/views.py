from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User

from .models import Profile
from .serializers import *
from .permissions import IsOwnerOrReadOnly


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUser(CreateAPIView):
    serializer_class = RegisterSerializer

class UpdatePassword(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            if not user.check_password(old_password):
                return Response({"message": "Wrong password"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
    
class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    

class ProfileDetail(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'profile_name'

class ProfileSearch(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        profile_name = self.request.query_params.get('search_key')
        if profile_name is not None:
            queryset = queryset.filter(profile_name__contains=profile_name)
        return queryset
    
#FOLLOW

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_profile(request, profile_name):
    profile = Profile.objects.get(user=request.user)
    if profile_name != profile.profile_name or \
        request.data['follow_from'] != profile.profile_name:
        return Response({"error": "Wrong profile name"},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = FollowCreateSerializer(data=request.data)
    if serializer.is_valid():
        follow = serializer.save()
        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)