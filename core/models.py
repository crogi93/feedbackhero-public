import os
import uuid

from django.db import models
from django.contrib.auth.models import User


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def upload_path(instance, filename):
    klass = type(instance).__name__
    *_, ext = os.path.splitext(filename)
    return 'images/{0}_{1}.{2}'.format(klass, uuid.uuid4(), ext)

class Board(TimestampMixin):
    name = models.CharField(max_length=255, unique=True)
    logo = models.FileField(upload_to=upload_path, blank=True, null=True)
    description = models.TextField()

class Status(TimestampMixin):
    name = models.CharField(max_length=255, unique=True)
    board = models.ForeignKey(Board, related_name='status', on_delete=models.DO_NOTHING)

class Suggestion(TimestampMixin):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000, blank=True, default='')
    image = models.FileField(upload_to=upload_path, blank=True, null=True)
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    author_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True)

class Comment(TimestampMixin):
    body = models.TextField(max_length=1000, blank=True, default='')
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    author_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    suggestion = models.ForeignKey(Suggestion, related_name='comments', on_delete=models.DO_NOTHING)

class Vote(TimestampMixin):
    suggestion = models.ForeignKey(Suggestion, related_name='votes', on_delete=models.DO_NOTHING)
