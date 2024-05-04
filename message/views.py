from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Message
from .serializers import MessageCreateSerializer, InboxItemSerializer, \
    MessageSerializer

from account.models import Profile

#post, 
# class MessageDetail()

class MessageList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender = self.request.user.profile
        receiver = get_object_or_404(Profile, id=self.kwargs['profile_other_id'])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['sender'] != sender.profile_name:
                return Response({"error": "You can only send messages as yourself."}, 
                                status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['receiver'] != receiver.profile_name:
                return Response({"error": "You can only send messages to the intended receiver."},
                                status=status.HTTP_400_BAD_REQUEST)
            message = serializer.save()
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        profile_other = get_object_or_404(Profile, id=self.kwargs['profile_other_id'])
        profile_me = self.request.user.profile
        messages = Message.objects.filter((Q(sender=profile_other) & Q(receiver=profile_me)) | 
                                          (Q(sender=profile_me) & Q(receiver=profile_other))) \
                                            .filter(deleted=False) \
                                            .order_by('-sent_at')
        data = {
            "profile_me": profile_me,
            "profile_other": profile_other,
            "messages": messages
        }
        return data

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        else:
            return InboxItemSerializer