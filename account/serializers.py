from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Profile, Follow

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email',
                  'first_name', 'last_name']
        extra_kwagrs = {
            'fist_name': {'required: True'},
            'last_name': {'required: True'}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields did not match."}
            )
        validate_password(attrs['password'])
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, profile_name=user.username)
        return user

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password']

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'profile_name', 'bio', 'profile_picture']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        depth = 1

class FollowCreateSerializer(serializers.Serializer):
    follow_from = serializers.CharField()
    follow_to = serializers.CharField()

    def validate(self, attrs):
        if attrs['follow_from'] == attrs['follow_to']:
            raise serializers.ValidationError(
                {"error": "Can't follow yourself"})
        return super().validate(attrs)

    def create(self, validated_data):
        profile_from = get_object_or_404(Profile, profile_name=validated_data['follow_from'])
        profile_to = get_object_or_404(Profile, profile_name=validated_data['follow_to'])

        try:
            follow = Follow.objects.get(follow_from=profile_from, follow_to=profile_to)
            follow.delete()
            return follow
        except: pass

        follow = Follow.objects.create(follow_from=profile_from, follow_to=profile_to)
        follow.save()
        return follow
