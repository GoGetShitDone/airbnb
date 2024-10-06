from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            'pk', 'country', 'city', 'name', 'host', 'price', 'address',
            'start', 'end', 'description', 'category',
            'created_at', 'updated_at'
        )
        read_only_fields = ('pk', 'created_at', 'updated_at')