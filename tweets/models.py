from django.db import models
from common.models import CommonModel


class Tweet(CommonModel):
    payload = models.TextField()

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.payload} from {self.user}"


class Like(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    liked_tweet = models.ForeignKey(
        "Tweet",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} likes {self.liked_tweet}"
