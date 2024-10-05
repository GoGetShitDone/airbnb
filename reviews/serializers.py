from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('pk', 'room', 'experience', 'payload', 'rating', 'created_at', 'updated_at')
        read_only_fields = ('pk', 'created_at', 'updated_at')