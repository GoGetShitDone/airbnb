from django.contrib import admin
from .models import Review


class RatingFilter(admin.SimpleListFilter):

    title = "Rating Category"

    parameter_name = "rating_category"

    def lookups(self, request, model_admin):
        return [
            ("perfect", "Perfect",),
            ("good", "Good",),
            ("bad", "Bad",),
        ]

    def queryset(self, request, queryset):
        if self.value() == "perfect":
            return queryset.filter(rating__gte=5)
        elif self.value() == "good":
            return queryset.filter(rating__in=[3, 4])
        elif self.value() == "bad":
            return queryset.filter(rating__in=[1, 2])


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        RatingFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
