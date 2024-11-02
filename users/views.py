import jwt
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from users.models import User
from . import serializers
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
import logging


logger = logging.getLogger(__name__)


class Me(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class Users(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        users = User.objects.all().order_by('id')
        serializer = serializers.TinyUserSerializer(users, many=True)
        data = {
            "authenticated_user": request.user.username if request.user.is_authenticated else None,
            "users": serializer.data
        }
        return Response(data)

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializers.PrivateUserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class UserTweets(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound
        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Add user data to response
            serializer = serializers.PrivateUserSerializer(user)
            return Response({
                "ok": "Welcome!",
                "user": serializer.data
            })
        else:
            return Response(
                {"error": "Wrong username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class JWTLogIn(APIView):
    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            token = jwt.encode(
                {
                "pk": user.pk,
                "exp": datetime.utcnow() + timedelta(hours=2),
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})

        else:
            return Response({"error": "wrong password"})


#########################
#########################
#########################

@method_decorator(csrf_exempt, name='dispatch')
class GithubLogIn(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        try:
            code = request.data.get("code")
            if not code:
                return Response(
                    {"error": "Code not provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Github Access Token 요청
            token_request = requests.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "code": code,
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GH_SECRET,
                    "scope": "user user:email",  # scope 추가
                },
                headers={"Accept": "application/json"},
            )

            token_json = token_request.json()
            
            # 디버깅을 위한 로그
            logger.info(f"GitHub Token Response: {token_json}")
            
            access_token = token_json.get("access_token")
            if not access_token:
                return Response(
                    {"error": "Access token not found", "details": token_json}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Github 사용자 정보 요청
            user_response = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                }
            )
            
            if not user_response.ok:
                return Response(
                    {"error": "Failed to get user data from GitHub"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_data = user_response.json()
            
            # 디버깅을 위한 로그
            logger.info(f"GitHub User Data: {user_data}")
            
            user = self.get_or_create_user(user_data, access_token)
            if user:
                login(request, user)
                return Response({"ok": "Welcome!"})
            else:
                return Response(
                    {"error": "Failed to create user"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API Error: {str(e)}")
            return Response(
                {"error": "Failed to communicate with GitHub"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_or_create_user(self, user_data, access_token):
        try:
            logger.info("Starting get_or_create_user") # 로깅 추가
            # Github 이메일 가져오기
            emails_response = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                }
            )
            
            if not emails_response.ok:
                logger.error(f"Failed to get GitHub emails: {emails_response.text}")
                return None
            
            emails = emails_response.json()
            
            # 디버깅을 위한 로그
            logger.info(f"GitHub Emails: {emails}")
            
            # 이메일 찾기 로직 개선
            primary_email = None
            
            # 먼저 primary 이메일 찾기
            for email in emails:
                if email.get("primary") and email.get("verified"):
                    primary_email = email.get("email")
                    break
            
            # primary 이메일이 없다면 첫 번째 verified 이메일 사용
            if not primary_email:
                for email in emails:
                    if email.get("verified"):
                        primary_email = email.get("email")
                        break
            
            if not primary_email:
                logger.error("No verified email found from GitHub")
                return None

            # 사용자 생성 또는 업데이트
            try:
                user = User.objects.get(email=primary_email)
                # 기존 사용자 정보 업데이트
                user.name = user_data.get("name") or user_data.get("login")
                user.avatar = user_data.get("avatar_url")
                user.save()
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=primary_email,
                    name=user_data.get("name") or user_data.get("login"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
            
            return user

        except Exception as e:
            logger.error(f"Error in get_or_create_user: {str(e)}")
            return None


#########################
#########################
#########################

@method_decorator(csrf_exempt, name='dispatch')
class KakaoLogIn(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        try:
            code = request.data.get("code")
            if not code:
                return Response(
                    {"error": "Code not provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 카카오 Access Token 요청
            token_request = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
                headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
            )

            token_json = token_request.json()
            
            # 디버깅을 위한 로그
            logger.info(f"Kakao Token Response: {token_json}")
            
            error = token_json.get("error")
            if error:
                logger.error(f"Failed to get Kakao token: {error}")
                return Response(
                    {"error": "Failed to get access token from Kakao", "details": error},
                    status=status.HTTP_400_BAD_REQUEST
                )

            access_token = token_json.get("access_token")
            if not access_token:
                return Response(
                    {"error": "Access token not found", "details": token_json}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 카카오 사용자 정보 요청
            user_response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                }
            )
            
            if not user_response.ok:
                logger.error(f"Failed to get Kakao user data: {user_response.text}")
                return Response(
                    {"error": "Failed to get user data from Kakao"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_data = user_response.json()
            
            # 디버깅을 위한 로그
            logger.info(f"Kakao User Data: {user_data}")
            
            user = self.get_or_create_user(user_data)
            if user:
                login(request, user)
                return Response({"ok": "Welcome!"})
            else:
                return Response(
                    {"error": "Failed to create user"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Kakao API Error: {str(e)}")
            return Response(
                {"error": "Failed to communicate with Kakao"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error during Kakao login: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_or_create_user(self, user_data):
        try:
            kakao_account = user_data.get("kakao_account")
            if not kakao_account:
                logger.error("No kakao_account data found")
                return None

            profile = kakao_account.get("profile")
            if not profile:
                logger.error("No profile data found")
                return None

            email = kakao_account.get("email")
            if not email:
                # 이메일이 없는 경우 카카오 ID를 사용하여 고유 이메일 생성
                kakao_id = user_data.get('id')
                email = f"kakao_{kakao_id}@kakao.user"
                logger.info(f"Generated email for Kakao user: {email}")

            try:
                user = User.objects.get(email=email)
                user.name = profile.get("nickname", user.name)
                user.avatar = profile.get("profile_image_url", user.avatar)
                user.save()
                logger.info(f"Updated existing user: {user.email}")
            except User.DoesNotExist:
                user = User.objects.create(
                    username=f"kakao_{user_data.get('id')}",
                    email=email,
                    name=profile.get("nickname", "Kakao User"),
                    avatar=profile.get("profile_image_url", ""),
                )
                user.set_unusable_password()
                user.save()
                logger.info(f"Created new user: {user.email}")
            
            return user

        except Exception as e:
            logger.error(f"Error in get_or_create_user: {str(e)}")
            return None


#########################
#########################
#########################

@method_decorator(csrf_exempt, name='dispatch')
class SignUp(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        try:
            logger.info(f"SignUp request received - Data: {request.data}") # 디버깅 로깅
            
            password = request.data.get("password")
            if not password:
                return Response(
                    {"error": "Password is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            username = request.data.get("username")
            email = request.data.get("email")
            name = request.data.get("name")
            
            # 사용자 생성
            user = User.objects.create(
                username=username,
                email=email,
                name=name,
            )
            user.set_password(password)
            user.save()
            
            # 로그인 처리
            login(request, user)
            
            logger.info(f"User created successfully: {username}")
            return Response({"ok": "User created successfully"})
            
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )