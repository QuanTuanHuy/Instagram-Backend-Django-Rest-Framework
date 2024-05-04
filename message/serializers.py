from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Message

from account.models import Profile
from account.serializers import ProfileSerializer

class MessageCreateSerializer(serializers.Serializer):
    sender = serializers.CharField()
    receiver = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        sender = get_object_or_404(Profile, profile_name=validated_data['sender'])
        receiver = get_object_or_404(Profile, profile_name=validated_data['receiver'])
        message = Message.objects.create(sender=sender, receiver=receiver, content=validated_data['content'])
        message.save()
        return message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['sender_name', 'receiver_name', 'content', 'sent_at', 'updated_at', 'seen', 'deleted']
    
    def get_sender_name(self, obj):
        sender = obj.sender.user
        return sender.first_name + ' ' + sender.last_name
    
    def get_receiver_name(self, obj):
        receiver = obj.receiver.user
        return receiver.first_name + ' ' + receiver.last_name

class InboxItemSerializer(serializers.Serializer):
    profile_me = ProfileSerializer()
    profile_other = ProfileSerializer()
    messages = serializers.ListField(child=MessageSerializer())
