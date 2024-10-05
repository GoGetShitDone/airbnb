from django.urls import path
from . import views

urlpatterns = [
    # Tweet URLs
    path("", views.TweetViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("<int:pk>", views.TweetViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    
    # Like URLs
    path("likes/", views.LikeViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("likes/<int:pk>", views.LikeViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    })),
]

# # 라우터 사용 버전 
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r'tweets', views.TweetViewSet)
# router.register(r'likes', views.LikeViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]