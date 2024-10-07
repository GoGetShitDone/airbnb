from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated

class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    ### Mission Code ###
    # def put(self, request, pk):
    #     room = self.get_object(pk)
    #     if not request.user.is_authenticated:
    #         raise NotAuthenticated
    #     if room.owner != request.user:
    #         raise PermissionDenied

    def put(self, request, pk):
        # 기존: amenity = self.get_object(pk)
        # 변경: Room 객체를 가져옵니다.
        room = self.get_object(pk)
        
        # 새로 추가: 사용자 인증 확인
        if not request.user.is_authenticated:
            raise NotAuthenticated
        
        # 새로 추가: 방 소유자 확인
        if room.owner != request.user:
            raise PermissionDenied
        
        # 기존: AmenitySerializer 사용
        # 변경: RoomDetailSerializer 사용, partial=True로 부분 업데이트 허용
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            # 새로 추가: 카테고리 업데이트 로직
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                    room.category = category
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            
            try:
                # 새로 추가: 트랜잭션 처리로 데이터 일관성 보장
                with transaction.atomic():
                    # 기존: updated_amenity = serializer.save()
                    # 변경: Room 객체 저장
                    updated_room = serializer.save()
                    
                    # 새로 추가: 편의시설(amenities) 업데이트 로직
                    amenities = request.data.get("amenities")
                    if amenities:
                        updated_room.amenities.clear()  # 기존 편의시설 모두 제거
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)  # 새 편의시설 추가
                    
                    # 기존: AmenitySerializer(updated_amenity).data
                    # 변경: RoomDetailSerializer로 업데이트된 방 정보 반환
                    return Response(RoomDetailSerializer(updated_room).data)
            # 새로 추가: 존재하지 않는 Amenity에 대한 예외 처리
            except Amenity.DoesNotExist:
                raise ParseError("Amenity not found")
        else:
            # 변경 없음: 유효성 검사 실패 시 에러 반환
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)

class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)



# test word 01

# {
# "name":"Hey~ This is test",
# "country":"Seoul",
# "city":"Seoul kangnam",
# "price":"100",
# "rooms":"2",
# "toilets":"2",
# "description":"GooD",
# "address":"YHEE",
# "pet_friendly":"true",
# "category":1,
# "amenities":[2,3],
# "kind":"private_room"
# }


# test word 02 - About PUT 

# {
#   "name": "Updated Room Name",
#   "price": 2500,
#   "description": "This is an updated description for the room.",
#   "category": 1,
#   "amenities": [2, 3] 
# }