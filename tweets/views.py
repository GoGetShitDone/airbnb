from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction
from .models import Tweet, Like
from .serializers import TweetSerializer, LikeSerializer
from users.models import User
from django.shortcuts import get_object_or_404

class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            all_tweets, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    tweet = serializer.save(user=request.user)
                    return Response(
                        TweetSerializer(tweet, context={'request': request}).data, 
                        status=status.HTTP_201_CREATED
                    )
            except Exception:
                return Response({"error": "Error creating tweet"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Tweet, pk=pk)

    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        tweet = self.get_object(pk)
        if request.user != tweet.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TweetSerializer(
            tweet, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetSerializer(updated_tweet, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if request.user != tweet.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TweetLikes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Tweet, pk=pk)

    def post(self, request, pk):
        tweet = self.get_object(pk)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    like, created = Like.objects.get_or_create(
                        user=request.user,
                        liked_tweet=tweet
                    )
                    action = "liked" if created else "already liked"
                    return Response({"message": f"Tweet {action}"}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Error liking tweet"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        try:
            like = Like.objects.get(user=request.user, liked_tweet=tweet)
            like.delete()
            return Response({"message": "Tweet unliked"}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)