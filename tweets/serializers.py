from rest_framework import serializers
from .models import Tweet, Like
from users.models import User


class TinyUserSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField()


class TweetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user = TinyUserSerializer(read_only=True)
    payload = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_is_liked(self, tweet):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, liked_tweet=tweet).exists()
        return False

    def get_likes_count(self, tweet):
        return tweet.likes.count()

    def create(self, validated_data):
        return Tweet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.payload = validated_data.get('payload', instance.payload)
        instance.save()
        return instance


class LikeSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user = TinyUserSerializer(read_only=True)
    liked_tweet = serializers.PrimaryKeyRelatedField(
        queryset=Tweet.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Like.objects.create(**validated_data)
