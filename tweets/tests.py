from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Tweet

class TweetsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.tweet = Tweet.objects.create(payload='Test tweet', user=self.user)
        self.tweets_url = reverse('tweets')
        self.tweet_detail_url = reverse('tweet_detail', kwargs={'pk': self.tweet.pk})

    def test_get_tweets(self):
        response = self.client.get(self.tweets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['payload'], 'Test tweet')

    def test_create_tweet(self):
        data = {'payload': 'New test tweet'}
        response = self.client.post(self.tweets_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 2)
        self.assertEqual(response.data['payload'], 'New test tweet')

    def test_get_tweet_detail(self):
        response = self.client.get(self.tweet_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload'], 'Test tweet')

    def test_update_tweet(self):
        data = {'payload': 'Updated test tweet'}
        response = self.client.put(self.tweet_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload'], 'Updated test tweet')

    def test_delete_tweet(self):
        response = self.client.delete(self.tweet_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tweet.objects.count(), 0)

    def test_create_tweet_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {'payload': 'Unauthenticated tweet'}
        response = self.client.post(self.tweets_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_tweet_unauthorized(self):
        unauthorized_user = User.objects.create_user(username='unauthorized', password='testpass')
        self.client.force_authenticate(user=unauthorized_user)
        data = {'payload': 'Unauthorized update'}
        response = self.client.put(self.tweet_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_tweet_unauthorized(self):
        unauthorized_user = User.objects.create_user(username='unauthorized', password='testpass')
        self.client.force_authenticate(user=unauthorized_user)
        response = self.client.delete(self.tweet_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)