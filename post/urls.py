from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.PostViewSet, basename='post')

urlpatterns = router.urls

# urlpatterns = [
#    path('', views.PostList.as_view(), name='post-list'),
#    path('<int:id>/change', ),
#    path('create', views.PostCreate.as_view(), name='post-create'),
# ]