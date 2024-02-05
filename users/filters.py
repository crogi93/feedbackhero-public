import django_filters

from core.models import Suggestion
from django.db import models


class SuggestionFilter(django_filters.FilterSet):
    class Meta:
        model = Suggestion
        fields = {
            "created_at": ["exact"],
            "title": ["exact"],
            "status__name": ["exact"],
        }
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            }
        }
