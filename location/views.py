from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS

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