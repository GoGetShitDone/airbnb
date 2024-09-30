from django.db import models
from common.models import CommonModel

# Tweet / tweet, like


class Tweet(CommonModel):
    payload = models.TextField()

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tweets",
    )

    def __str__(self):
        return f"{self.payload} from {self.user}"


class Like(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    liked_tweet = models.ForeignKey(
        "Tweet",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    def __str__(self):
        return f"{self.user} likes {self.liked_tweet}"
