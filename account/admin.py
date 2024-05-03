from django.contrib import admin
from .models import Follow, Profile

# Register your models here.
@admin.register(Profile)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_picture']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follow_from', 'follow_to', 'created']