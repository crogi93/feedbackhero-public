from django.db import models
from django.dispatch import receiver

from core.models import *


@receiver(models.signals.post_delete, sender=Board)
@receiver(models.signals.post_delete, sender=Suggestion)
def auto_delete_file_on_delete(sender, instance, **kwargs) -> None:
    if instance.thumbnail:
        instance.thumbnail.delete(False)


@receiver(models.signals.pre_save, sender=Board)
@receiver(models.signals.pre_save, sender=Suggestion)
def auto_delete_file_on_change(sender, instance, **kwargs) -> None:
    if instance.pk is None:
        return
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.thumbnail is None:
        return

    if old_instance.thumbnail != instance.thumbnail:
        old_instance.thumbnail.delete(False)
