from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/likes', views.profile_liked, name='profile_liked'),
    path('posts/<int:post_id>/comments', views.profile_liked, name='comments_in_post'),

    path('create_like/', views.like_create, name='like_create'),
    path('create_commment/', views.comment_create, name='comment_create'),

    path('your_activity/posts/', views.history_post, name='history_post'),
    path('your_activity/likes/', views.history_likes, name='history_likes'),
    path('your_activity/comments/', views.history_comments, name='history_comments'),
]
