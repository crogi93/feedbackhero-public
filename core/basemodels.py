from django.db import models
from datetime import datetime


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def is_deleted(self) -> bool:
        return self.deleted_at

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now()
