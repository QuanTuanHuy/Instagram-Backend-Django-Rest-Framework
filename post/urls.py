from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/likes/', views.profile_liked, name='profile_liked'),
    path('posts/<int:post_id>/comments/', views.comments_in_post, name='comments_in_post'),

    path('create_like/', views.like_create, name='like_create'),
    path('comments/create_comment/', views.comment_create, name='comment_create'),
    path('comments/delete_comment/', views.delete_comment, name='delete_comment'),

    path('your_activity/posts/', views.history_post, name='history_post'),
    path('your_activity/saved/', views.post_saved, name='post_saved'),
    # path('your_activity/tagged/', views.tagged, name='tagged'),
    path('your_activity/likes/', views.history_likes, name='history_likes'),
    path('your_activity/comments/', views.history_comments, name='history_comments'),
]
