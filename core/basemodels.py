from datetime import datetime

import yaml
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.db import models


def dict_to_choices(input_dict_list):
    return tuple(
        (key, value) for item in input_dict_list for key, value in item.items()
    )


def get_icon_list():
    file = find(settings.ICON_YAML_FILE)
    if not file:
        raise ValueError(
            "Can't find {}, \
            check ICON_YAML_FILE setting.".format(
                settings.ICON_YAML_FILE
            )
        )
    with open(file, "r", encoding="utf-8") as stream:
        data_loaded = yaml.load(stream, Loader=yaml.SafeLoader)
    return dict_to_choices(data_loaded)


ICON_CHOICES = get_icon_list()


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


class IconField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 50)
        kwargs.setdefault("choices", ICON_CHOICES)
        super().__init__(*args, **kwargs)
