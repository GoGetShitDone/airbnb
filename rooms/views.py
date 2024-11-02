from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from . import serializers
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = serializers.RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        print("Received data:", request.data)  # 받은 데이터 확인
        
        if not request.user.is_authenticated:
            return Response({"detail": "Please log in."}, status=401)
            
        serializer = serializers.RoomDetailSerializer(
            data=request.data,
            context={"request": request}
        )
        
        print("Is valid:", serializer.is_valid())  # 유효성 검사 결과
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # 유효성 검사 에러
            return Response(serializer.errors, status=400)
            
        try:
            category_pk = request.data.get("category")
            print("Category PK:", category_pk)  # 카테고리 PK 확인
            
            if not category_pk:
                raise ParseError("Category is required.")
                
            category = Category.objects.get(pk=category_pk)
            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The category kind should be 'rooms'")

            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    print("Room created:", room)  # 생성된 방 정보

                    # amenities 처리
                    amenities = request.data.get("amenities")
                    print("Received amenities:", amenities)  # amenities 데이터 확인
                    
                    if amenities:
                        # 리스트가 아니면 리스트로 변환
                        if not isinstance(amenities, list):
                            amenities = [amenities]
                        
                        # 유효한 amenity_pks만 필터링
                        valid_amenity_pks = [
                            pk for pk in amenities 
                            if pk is not None and str(pk).isdigit()
                        ]
                        
                        print("Valid amenity PKs:", valid_amenity_pks)  # 유효한 amenity PKs 확인
                        
                        if valid_amenity_pks:
                            for amenity_pk in valid_amenity_pks:
                                try:
                                    amenity = Amenity.objects.get(pk=amenity_pk)
                                    room.amenities.add(amenity)
                                except Amenity.DoesNotExist:
                                    print(f"Amenity {amenity_pk} not found")  # 없는 amenity 확인
                                    continue

                    return Response(
                        serializers.RoomDetailSerializer(
                            room,
                            context={"request": request}
                        ).data
                    )
            except Exception as room_error:
                print(f"Error saving room: {str(room_error)}")  # 방 저장 중 에러
                raise ParseError(f"Error saving room: {str(room_error)}")
                
        except Category.DoesNotExist:
            print("Category not found")  # 카테고리 없음
            raise ParseError("Category not found")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # 예상치 못한 에러
            raise ParseError(f"Cannot create room: {str(e)}")

class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = serializers.RoomDetailSerializer(
            room, 
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        
        if room.owner != request.user:
            raise PermissionDenied
        
        serializer = serializers.RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        
        if serializer.is_valid():
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
                with transaction.atomic():
                    updated_room = serializer.save()
                    amenities = request.data.get("amenities")
                    if amenities:
                        if not isinstance(amenities, list):
                            amenities = [amenities]
                        
                        updated_room.amenities.clear()
                        valid_amenity_pks = [
                            pk for pk in amenities 
                            if pk is not None and str(pk).isdigit()
                        ]
                        
                        for amenity_pk in valid_amenity_pks:
                            try:
                                amenity = Amenity.objects.get(pk=amenity_pk)
                                updated_room.amenities.add(amenity)
                            except Amenity.DoesNotExist:
                                print(f"Amenity {amenity_pk} not found")
                                continue
                                
                    return Response(
                        serializers.RoomDetailSerializer(
                            updated_room,
                            context={"request": request}
                        ).data
                    )
            except Exception as e:
                raise ParseError(f"Error updating room: {str(e)}")
        else:
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
        serializer = serializers.AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                serializers.AmenitySerializer(amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                serializers.AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()

        # 모든 예약정보 확인
        all_bookings = Booking.objects.filter(room=room)

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gte=now,
        )

        # 디버깅 정보를 포함
        debug_info = {
            "current_date": now,
            "total_bookings": all_bookings.count(),
            "filtered_bookings": bookings.count(),
            "all_bookings_dates": list(all_bookings.values_list('check_in', flat=True)),
            "filtered_bookings_dates": list(bookings.values_list('check_in', flat=True)),
        }

        serializer = PublicBookingSerializer(bookings, many=True)

        return Response({
            "debug_info" : debug_info,
            "bookings": serializer.data
            })

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
