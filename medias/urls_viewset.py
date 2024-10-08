from django.urls import path
from . import views

urlpatterns = [
    # Photo
    path("photos/", views.PhotoViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("photos/<int:pk>", views.PhotoViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    
    # Video
    path("videos/", views.VideoViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("videos/<int:pk>", views.VideoViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
]
