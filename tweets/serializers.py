from rest_framework import serializers
from .models import Tweet, Like
from users.models import User

class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')

class TweetSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ('pk', 'user', 'payload', 'created_at', 'updated_at', 'is_liked', 'likes_count')
        read_only_fields = ('pk', 'created_at', 'updated_at')

    def get_is_liked(self, tweet):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, liked_tweet=tweet).exists()
        return False

    def get_likes_count(self, tweet):
        return tweet.likes.count()

class LikeSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ('pk', 'user', 'liked_tweet', 'created_at', 'updated_at')
        read_only_fields = ('pk', 'created_at', 'updated_at')