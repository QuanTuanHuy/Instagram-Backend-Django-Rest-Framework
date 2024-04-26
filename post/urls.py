from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.PostList.as_view(), name='post-list'),
   path('create', views.PostCreate.as_view(), name='post-create'),
]