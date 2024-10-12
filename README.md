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


---

### 졸업과제 ~ 16.5 

#### Mission:
- Django Rest Framework을 사용하여, 아래와 같은 기능을 갖고있는 REST API 를 빌드하세요.

##### API Routes
ModelSerializer 그리고 APIView 를 사용하여 아래 routes 를 구현하세요.

[x] <!-- tweets -->
- GET /api/v1/tweets: See all tweets
- POST /api/v1/tweets: Create a tweet
- GET /api/v1/tweets/<int:pk>: See a tweet
- PUT /api/v1/tweets/<int:pk>: Edit a tweet
- DELETE /api/v1/tweets/<int:pk>: Delete a tweet

[x] <!-- users -->
- GET /api/v1/users: See all users
- POST /api/v1/users: Create a user account with password
- GET /api/v1/users/<int:pk>: See user profile
- GET /api/v1/users/<int:pk>/tweets: See tweets by a user
- PUT /api/v1/users/password: Change password of logged in user.
- POST /api/v1/users/login: Log user in
- POST /api/v1/users/logout: Log user out

##### Authentication [x]
- UsernameAuthentication라는 이름의 authentication class를 빌드하세요.
- UsernameAuthentication 는 반드시 BaseAuthentication에서 extend 되어야 합니다.
- X-USERNAME 헤더를 사용하는 유저를 찾으세요.

##### Testing [x]
다음과 같은 URL 과 메소드를 위한 APITestCase 를 작성하세요.
- /api/v1/tweets: Test GET and POST methods
- /api/v1/tweets/<int:pk>: Test GET, PUT and DELETE methods

---

# tweets.test.py 세부 내용

## 개요
- Tweet 관련 API 엔드포인트 테스트 코드.
- APITestCase 사용.
- /api/v1/tweets와 /api/v1/tweets/<int:pk> 엔드포인트 테스트.

## 테스트 케이스

1. test_get_tweets
   - 목적: 모든 트윗 조회 테스트.
   - 메소드: GET
   - URL: /api/v1/tweets
   - 예상 결과: 200 OK, 생성된 트윗 목록 반환.

2. test_create_tweet
   - 목적: 새 트윗 생성 테스트.
   - 메소드: POST
   - URL: /api/v1/tweets
   - 데이터: {'payload': 'New test tweet'}
   - 예상 결과: 201 Created, 새 트윗 정보 반환.

3. test_get_tweet_detail
   - 목적: 특정 트윗 상세 조회 테스트.
   - 메소드: GET
   - URL: /api/v1/tweets/<int:pk>
   - 예상 결과: 200 OK, 해당 트윗 정보 반환.

4. test_update_tweet
   - 목적: 트윗 수정 테스트.
   - 메소드: PUT
   - URL: /api/v1/tweets/<int:pk>
   - 데이터: {'payload': 'Updated test tweet'}
   - 예상 결과: 200 OK, 수정된 트윗 정보 반환.

5. test_delete_tweet
   - 목적: 트윗 삭제 테스트.
   - 메소드: DELETE
   - URL: /api/v1/tweets/<int:pk>
   - 예상 결과: 204 No Content.

6. test_create_tweet_unauthenticated
   - 목적: 인증되지 않은 사용자의 트윗 생성 시도 테스트.
   - 메소드: POST
   - URL: /api/v1/tweets
   - 예상 결과: 403 Forbidden.

7. test_update_tweet_unauthorized
   - 목적: 권한 없는 사용자의 트윗 수정 시도 테스트.
   - 메소드: PUT
   - URL: /api/v1/tweets/<int:pk>
   - 예상 결과: 403 Forbidden.

8. test_delete_tweet_unauthorized
   - 목적: 권한 없는 사용자의 트윗 삭제 시도 테스트.
   - 메소드: DELETE
   - URL: /api/v1/tweets/<int:pk>
   - 예상 결과: 403 Forbidden.

## 설정
- setUp 메소드에서 테스트용 사용자와 트윗 생성.
- 인증된 사용자로 대부분의 테스트 실행.
