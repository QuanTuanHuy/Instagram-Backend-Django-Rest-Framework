from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS

from django.shortcuts import get_object_or_404

from post.models import Post
from post.serializers import PostSerializer

from .models import Place
from .serializers import PlaceSerializers
from .permissions import IsAdminUserOrReadOnly

class PlaceList(ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers
    permission_classes = [IsAdminUserOrReadOnly]

class PlaceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']
        return get_object_or_404(Place, pk=pk, slug=slug)
    
