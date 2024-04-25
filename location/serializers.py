from rest_framework import serializers
from django.utils.text import slugify
from .models import Place

class PlaceSerializers(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Place
        fields = ['name', 'slug', 'longitude', 'latitude']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)