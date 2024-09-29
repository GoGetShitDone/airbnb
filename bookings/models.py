from django.db import models
from common.models import CommonModel


class Booking(CommonModel):
    """Booking Model Definition"""
    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"
    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    # 1명의 유저는 많은 부킹을 가질 수 있으나, 부킹은 오직 하나의 유저만 활성화 해야함! -> ForeignKey
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    experience_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kind.title()} booking for: {self.user}"
