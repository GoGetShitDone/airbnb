from django.urls import path
from . import views

urlpatterns = [
    # Room url
    path("", views.Rooms.as_view()),

    # Amenity urls
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
    
]
