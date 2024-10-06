from django.urls import path
from . import views

urlpatterns = [ 
    # Rooms URLs - ViewSet
    Room URLs
    path("", views.RoomViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("<int:pk>", views.RoomViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),

    # Amenity URLs - ViewSet
    path("amenity/", views.AmenityViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("amenity/<int:pk>", views.AmenityViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
]