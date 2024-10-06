from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/tweets/", include("tweets.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
]