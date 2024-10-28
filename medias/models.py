from django.db import models
from common.models import CommonModel

class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        if self.room:
            return f"Photo for Room: {self.room.name}"
        elif self.experience:
            return f"Photo for Experience: {self.experience.name}"
        return f"Photo {self.pk}"


class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.experience:
            return f"Video for Experience: {self.experience.name}"
        return f"Video {self.pk}"


# from django.db import models
# from common.models import CommonModel


# class Photo(CommonModel):
#     file = models.URLField()
#     description = models.CharField(
#         max_length=140,
#     )
#     room = models.ForeignKey(
#         "rooms.Room",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="photos",

#     )
#     experience = models.ForeignKey(
#         "experiences.Experience",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="photos",
#     )

#     def __str__(self):
#         return "Photo File"


# class Video(CommonModel):
#     file = models.URLField()
#     experience = models.OneToOneField(
#         "experiences.Experience",
#         on_delete=models.CASCADE,
#     )

#     def __str__(self):
#         return "Video File"
