from django.contrib import admin
from .models import Tweet, Like


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
