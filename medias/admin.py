from django.contrib import admin
from django.utils.html import mark_safe
from .models import Photo, Video

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "thumbnail",
        "description",
        "get_room_name",
        "get_experience_name",
        "created_at",
    )
    
    list_display_links = (
        "pk",
        "description",
    )
    
    list_filter = (
        "created_at",
        "updated_at",
        "room__name",
        "experience__name",
    )
    
    search_fields = (
        "description",
        "room__name",
        "experience__name",
    )

    # 썸네일 표시
    def thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.file}" width="50" height="50" style="object-fit: cover;" />')
    thumbnail.short_description = "Photo"

    # Room 이름 표시
    def get_room_name(self, obj):
        if obj.room:
            return obj.room.name
        return "—"
    get_room_name.short_description = "Room"

    # Experience 이름 표시
    def get_experience_name(self, obj):
        if obj.experience:
            return obj.experience.name
        return "—"
    get_experience_name.short_description = "Experience"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "file",
        "get_experience_name",
        "created_at",
        "updated_at",
    )
    
    list_display_links = (
        "pk",
        "file",
    )
    
    list_filter = (
        "created_at",
        "updated_at",
        "experience__name",
    )
    
    search_fields = (
        "file",
        "experience__name",
    )

    def get_experience_name(self, obj):
        return obj.experience.name if obj.experience else "—"
    get_experience_name.short_description = "Experience"


# from django.contrib import admin
# from .models import Photo, Video


# @admin.register(Photo)
# class PhotoAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Video)
# class VideoAdmin(admin.ModelAdmin):
#     pass
