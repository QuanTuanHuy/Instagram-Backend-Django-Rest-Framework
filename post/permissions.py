from rest_framework import permissions
from .models import Post
from account.models import Profile

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == Profile.objects.get(user=request.user)