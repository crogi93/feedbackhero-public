import os
import uuid

from django.db import models

from core.basemodels import IconField, TimestampMixin
from customers.models import User


def upload_path(instance, filename):
    klass = type(instance).__name__
    *_, ext = os.path.splitext(filename)
    return "images/{0}_{1}{2}".format(klass, uuid.uuid4(), ext)


class Board(TimestampMixin):
    user = models.ForeignKey(User, related_name="board", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, unique=True)
    logo = models.FileField(upload_to=upload_path, blank=True, null=True)
    description = models.TextField()
    footer = models.JSONField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    @property
    def thumbnail(self):
        return self.logo


class Status(TimestampMixin):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, related_name="status", on_delete=models.DO_NOTHING)
    icon = IconField(null=True, blank=True)
    is_default = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_statusname_per_board"
            ),
            models.UniqueConstraint(
                fields=["board", "is_default"],
                condition=models.Q(is_default=True),
                name="unique_default_status_per_board",
            ),
        ]


class Suggestion(TimestampMixin):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    image = models.FileField(upload_to=upload_path, blank=True, null=True)
    status = models.ForeignKey(
        Status, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "title"], name="unique_suggestionstitle_per_board"
            )
        ]

    @property
    def thumbnail(self):
        return self.image


class Comment(TimestampMixin):
    body = models.TextField(max_length=1000)
    suggestion = models.ForeignKey(
        Suggestion, related_name="comments", on_delete=models.DO_NOTHING
    )


class Vote(TimestampMixin):
    suggestion = models.ForeignKey(
        Suggestion, related_name="votes", on_delete=models.DO_NOTHING
    )
