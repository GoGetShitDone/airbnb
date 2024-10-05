from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookingViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("<int:pk>", views.BookingViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
]