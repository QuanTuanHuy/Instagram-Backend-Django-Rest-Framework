from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
]