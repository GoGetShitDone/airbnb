from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Tweet, Like
from .serializers import TweetSerializer, LikeSerializer

class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Tweet, Like
# from .serializers import TweetSerializer, LikeSerializer
# from users.models import User
# from django.shortcuts import get_object_or_404

# @api_view(['GET', 'POST'])
# def tweets(request):
#     if request.method == 'GET':
#         all_tweets = Tweet.objects.all()
#         serializer = TweetSerializer(
#             all_tweets, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = TweetSerializer(
#             data=request.data, context={'request': request})
#         if serializer.is_valid():
#             try:
#                 user = User.objects.get(pk=request.user.pk)
#             except User.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#             tweet = serializer.save(user=user)
#             return Response(TweetSerializer(tweet, context={'request': request}).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE', 'POST'])
# def tweet(request, pk):
#     tweet = get_object_or_404(Tweet, pk=pk)

#     if request.method == 'GET':
#         serializer = TweetSerializer(tweet, context={'request': request})
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         if request.user != tweet.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         serializer = TweetSerializer(
#             tweet, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         if request.user != tweet.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         tweet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     elif request.method == 'POST':
#         action = request.data.get('action')
#         if action not in ['like', 'unlike']:
#             return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(pk=request.user.pk)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         if action == 'like':
#             like, created = Like.objects.get_or_create(
#                 user=user, liked_tweet=tweet)
#             return Response({"message": "Tweet liked"}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
#         elif action == 'unlike':
#             Like.objects.filter(user=user, liked_tweet=tweet).delete()
#             return Response({"message": "Tweet unliked"}, status=status.HTTP_200_OK)
