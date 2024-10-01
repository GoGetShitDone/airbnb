from django.contrib import admin
from django.db.models import Q
from .models import Tweet, Like


class AboutWordElon(admin.SimpleListFilter):

    title = "Mentions of Elon Musk"

    parameter_name = "elonmusk"

    def lookups(self, request, model_admin):
        return [
            ("contain", "Contain",),
            ("not_contain", "Not contain",),
        ]

    def queryset(self, request, queryset):
        if self.value() == "contain":
            return queryset.filter(Q(payload__icontains="Elon") | Q(payload__icontains="Musk"))
        elif self.value() == "not_contain":
            return queryset.exclude(Q(payload__icontains="Elon") | Q(payload__icontains="Musk"))
        return queryset


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

    list_filter = (
        "created_at",
        AboutWordElon,
    )

    search_fields = (
        "payload",
        "user",
    )

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

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user",
    )
