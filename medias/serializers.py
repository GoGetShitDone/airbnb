from rest_framework import serializers
from .models import Photo, Video

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
            "room",
            "experience",
            "created_at",
        )
        read_only_fields = ('pk', 'created_at',)

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            "pk",
            "file",
            "experience",
            "created_at",
        )
        read_only_fields = ('pk', 'created_at',)