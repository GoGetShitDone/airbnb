from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    """Wishlist Model Definition"""
    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlist",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlist",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlist",
    )

    def __str__(self) -> str:
        return self.name
