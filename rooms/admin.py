from django.contrib import admin
from .models import Room, Amenity
from medias.models import Photo # 이 import 추가

class PhotoInline(admin.TabularInline):  # Inline 클래스 추가
    model = Photo
    extra = 0
    fields = ("file", "description")

@admin.action(description="Set all prices to Zero")
def reset_prices(model_admin, request, rooms,):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)  # inlines 추가
    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
        "review_count",
        "rating",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "^price",
        "=owner__username",
    )

    # models 에도 아래와 같은 기능의 함수가 존재함!
    # def total_amenities(self, room):
    #     return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
