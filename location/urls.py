from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlaceList.as_view(), name='location-list'),
    path('<int:pk>/<slug:slug>/all_posts/', views.PostInPlace.as_view(),
         name='post-in-location'),
    path('<int:pk>/<slug:slug>', views.PlaceDetail.as_view(),
         name='location-detail'),
]