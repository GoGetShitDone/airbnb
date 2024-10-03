from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Tweet, Like
from .serializers import TweetSerializer, LikeSerializer


@api_view(["GET", "POST"])
def tweets(request):
    if request.method == "GET":
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            all_tweets, many=True, context={"request": request})
        return Response(serializer.data)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            raise NotAuthenticated
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            new_tweet = serializer.save(user=request.user)
            return Response(TweetSerializer(new_tweet).data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE", "POST"])
def tweet(request, pk):
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = TweetSerializer(tweet, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PUT":
        if not request.user.is_authenticated or request.user != tweet.user:
            raise NotAuthenticated
        serializer = TweetSerializer(
            tweet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetSerializer(updated_tweet).data)
        else:
            return Response(serializer.errors)

    elif request.method == "DELETE":
        if not request.user.is_authenticated or request.user != tweet.user:
            raise NotAuthenticated
        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            raise NotAuthenticated

        action = request.data.get('action')
        if not action:
            raise ParseError("'action' field is required")

        if action == "like":
            if Like.objects.filter(user=request.user, liked_tweet=tweet).exists():
                return Response({"detail": "You have already liked this tweet."})
            Like.objects.create(user=request.user, liked_tweet=tweet)
            return Response({"detail": "Tweet liked successfully."})

        elif action == "unlike":
            try:
                like = Like.objects.get(user=request.user, liked_tweet=tweet)
            except Like.DoesNotExist:
                return Response({"detail": "You haven't liked this tweet."})
            like.delete()
            return Response({"detail": "Tweet unliked successfully."})

        else:
            raise ParseError("Invalid action. Use 'like' or 'unlike'.")
