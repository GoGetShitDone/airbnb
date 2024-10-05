from rest_framework import serializers
from .models import Room, Amenity
from users.models import User

class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')

class RoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = (
            'pk', 'name', 'country', 'city', 'price', 'rooms', 'toilets',
            'description', 'address', 'pet_friendly', 'kind', 'user',
            'amenities', 'category', 'created_at', 'updated_at'
        )
        read_only_fields = ('pk', 'created_at', 'updated_at')

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('pk', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('pk', 'created_at', 'updated_at')
