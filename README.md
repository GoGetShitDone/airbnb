# airbnb
Airbnb clone coding


# Refactoring - v1 / 10.05, Sat(start) -> ing
## ViewSet -> APIVIew 로 변경됨! 
### 리팩토링 순서 : 모델 확인 -> 시리얼라이저 -> 뷰s -> urls

## 1. catefories [x]
## 2. tweets [x]
## 3. rooms [x]
## 4. users [x]
## 5. booking [x]
## 6. experiences [x]
## 7. medias [x]
## 8. reviews [x]
## 9. wishlists [x]



# 참고 

### Rooms 
- 11.4 - amenity 관련 url 만들어야함! 

### Users
- [ ] GET PUT /me
- [ ] POST /user
- [ ] POST /user/username
- [ ] POST /user/log-in
- [ ] POST /user/change-password
- [ ] POST users/github

--- 

### Experiences (TODOS)

- [ ] POST /experiences
- [ ] GET PUT DELETE /experiences/1
- [ ] GET /experiences/1/perks
- [x] GET POST /perks
- [x] GET PUT DELETE /perks/1
- [ ] GET POST /experiences/1/bookings
- [ ] GET PUT DELETE /experiences/1/bookings/2


### 졸업과제 ~ 16.5 

#### Mission:
- Django Rest Framework을 사용하여, 아래와 같은 기능을 갖고있는 REST API 를 빌드하세요.

##### API Routes
ModelSerializer 그리고 APIView 를 사용하여 아래 routes 를 구현하세요.
<!-- tweets -->
- GET /api/v1/tweets: See all tweets
- POST /api/v1/tweets: Create a tweet
- GET /api/v1/tweets/<int:pk>: See a tweet
- PUT /api/v1/tweets/<int:pk>: Edit a tweet
- DELETE /api/v1/tweets/<int:pk>: Delete a tweet

<!-- users -->
- GET /api/v1/users: See all users
- POST /api/v1/users: Create a user account with password
- GET /api/v1/users/<int:pk>: See user profile
- GET /api/v1/users/<int:pk>/tweets: See tweets by a user
- PUT /api/v1/users/password: Change password of logged in user.
- POST /api/v1/users/login: Log user in
- POST /api/v1/users/logout: Log user out

##### Authentication
- UsernameAuthentication라는 이름의 authentication class를 빌드하세요.
- UsernameAuthentication 는 반드시 BaseAuthentication에서 extend 되어야 합니다.
- X-USERNAME 헤더를 사용하는 유저를 찾으세요.

##### Testing
다음과 같은 URL 과 메소드를 위한 APITestCase 를 작성하세요.
- /api/v1/tweets: Test GET and POST methods
- /api/v1/tweets/<int:pk>: Test GET, PUT and DELETE methods


# Authentications
4가지 방식의 Authenticate
- Session Authentication - 기본적으로 Django 제공
- Basic Authentication - Custom 가능하지만 사용 안함
- Token Authentication
- JWT Authentication

## 추천

### Token : django-rest-knox
### JWT : Simple JWT




# TEST 
- def test_create_amenity(self): 이 부분 작동이 이상함 
