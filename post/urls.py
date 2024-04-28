from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/likes', views.profile_liked, name='profile_liked'),
    path('likes/', views.like_create, name='create-like'),
    path('<str:profile_name>/posted', views.posted, name='posted'),
    path('<str:profile_name>/liked_post', views.liked_post, name='like-post'),
]
