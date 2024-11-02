from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.models import Category  # 이 줄 추가
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "id",
            "name",
            "description",
        )

class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all(),
        required=False,
    )
    # category = CategorySerializer(
    #     read_only=True,
    # )

    # 프론트 소통을 위해 임시 추가
    category_detail = CategorySerializer(
        read_only=True,
        source='category'
    )
    # 프론트 소통을 위해 임시 추가
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(kind=Category.CategoryKindChoices.ROOMS),
        required=True,
    )
    
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    # reviews = ReviewSerializer(many=True, read_only=True,)

    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
            "category_detail",

        )

    def get_rating(self, room):
        return room.rating()

    # 기존 get is_owner 코드 
    # def get_is_owner(self, room):
    #     request = self.context["request"]
    #     return room.owner == request.user

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        return False

    def get_is_liked(self, room):
        request = self.context.get("request")        
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    rooms__pk=room.pk,
                ).exists()
            return False

    # def get_is_liked(self, room):
    #     request = self.context.get("request")        
    #     if request: and request.user.is_authenticated:  # request 존재 여부 먼저 체크
    #         return Wishlist.objects.filter(
    #             user=request.user,
    #             rooms__pk=room.pk,
    #         ).exists()
    #     return False


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)


    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        return False