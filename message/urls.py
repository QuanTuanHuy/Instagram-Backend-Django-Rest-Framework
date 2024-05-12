from django.urls import include, path
from . import views

urlpatterns = [
    #list of all users who have received a message from the current user
    path('inbox/', views.all_profiles_inbox_with_me, name='inbox'),


    path('inbox/<int:profile_other_id>/messages/', views.MessageList.as_view(), name='inbox_detail'),


    path('inbox/<int:profile_other_id>/messages/<int:message_id>/', views.MessageDetail.as_view(), name='message_detail'),
]