from rest_framework import serializers
from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('pk', 'name', 'rooms', 'experiences', 'user',)
        read_only_fields = ('pk', 'created_at', 'updated_at')