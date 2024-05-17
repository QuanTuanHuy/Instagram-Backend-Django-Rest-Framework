from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .models import Message
from .serializers import MessageCreateSerializer, InboxItemSerializer, \
    MessageSerializer

from account.models import Profile
from account.serializers import ProfileSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_profiles_inbox_with_me(request):
    profile_me = request.user.profile
    other_profiles_chat_to_me = profile_me.received_messages.values_list('sender', flat=True).distinct()
    other_profiles_me_chat_to = profile_me.sent_messages.values_list('receiver', flat=True).distinct()
    other_profile_ids = other_profiles_chat_to_me.union(other_profiles_me_chat_to)
    
    response = []
    for profile_id in set(other_profile_ids):
        profile_other = Profile.objects.get(id=profile_id)
        last_message = Message.objects.filter((Q(sender=profile_other) & Q(receiver=profile_me)) | \
                                              (Q(sender=profile_me) & Q(receiver=profile_other))) \
                                              .filter(deleted=False).first()
        response.append([{"profile_other": ProfileSerializer(profile_other).data,
                         "last_message": MessageSerializer(last_message).data}])

    return Response(response, status=status.HTTP_200_OK)


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
                                            .filter(deleted=False)
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
        

class MessageDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_object(self):
        me = self.request.user.profile
        other = get_object_or_404(Profile, id=self.kwargs['profile_other_id'])

        message = get_object_or_404(Message, id=self.kwargs['message_id'])

        if (message.sender == me and message.receiver == other) or \
            (message.sender == other and message.receiver == me):
            return message
        
        return None
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender != self.request.user.profile:
            return Response({"error": "You can only update your own messages."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sender != self.request.user.profile:
            return Response({"error": "You can only delete your own messages."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        instance.deleted = True
        instance.save()
        return Response({"message": "Message deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)
    
#search
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_inbox(request, profile_other_id):
    profile_me = request.user.profile
    profile_other = get_object_or_404(Profile, id=profile_other_id)
    search_query = request.query_params.get('q', None)
    if search_query is None:
        return Response({"error": "No search query provided."},
                        status=status.HTTP_400_BAD_REQUEST)

    messages = Message.objects.filter((Q(sender=profile_other) & Q(receiver=profile_me)) | \
                                      (Q(sender=profile_me) & Q(receiver=profile_other)),
                                      content__icontains=search_query).filter(deleted=False)
    
    serializers = MessageSerializer(messages, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)