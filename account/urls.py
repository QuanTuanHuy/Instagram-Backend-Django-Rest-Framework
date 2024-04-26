from django.urls import include, path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('users/<int:pk>/change_password/', views.UpdatePassword.as_view(), name='change-password'),
    path('profiles/', views.ProfileList.as_view(), name='profile-list'),
    path('profiles/<str:profile_name>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profiles/search', views.ProfileSearch.as_view(), name='profile-search'),
]