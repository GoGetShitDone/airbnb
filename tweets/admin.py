from django.contrib import admin
from .models import Tweet, Like

# Tweet / tweet, like


@admin.register(Tweet)
class Tweet(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
        "user",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)


@admin.register(Like)
class Like(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "liked_tweet",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)
