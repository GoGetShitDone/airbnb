from django.contrib import admin
from .models import Tweet, Like

# Tweet / tweet, like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
        "user",
        "total_likes",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)

    def total_likes(self, obj):
        return obj.likes.count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "liked_tweet",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)
