from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("me", views.Me.as_view()), 
    path("signup", views.SignUp.as_view()),
    path("", views.Users.as_view()),
    path("<int:pk>", views.UserProfile.as_view()),
    path("<int:pk>/tweets", views.UserTweets.as_view()),
    path("password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("logout", views.LogOut.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogIn.as_view()),
    path("github", views.GithubLogIn.as_view()),
    path("kakao", views.KakaoLogIn.as_view()),
    path("@<str:username>", views.PublicUser.as_view())
]

