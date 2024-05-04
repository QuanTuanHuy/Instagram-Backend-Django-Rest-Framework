from django.urls import include, path
from . import views

urlpatterns = [
    #list of all users who have received a message from the current user
    # path('inbox/', views.InboxView.as_view(), name='inbox'),


    path('inbox/<int:profile_other_id>/', views.MessageList.as_view(), name='inbox_detail'),


    # path('inbox/<int:profile_received_id>/items/<int:message_id>/', views.MessageDetail.as_view(), name='message_detail'),
]