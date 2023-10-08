from typing import Optional

from rest_framework import serializers

from core.models import Board, Comment, Suggestion, Status, Vote


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ["created_at", "deleted_at", "updated_at"]
        fields = "__all__"


class StatusSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Status


class BoardSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Board


class SuggestionSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Suggestion


class CommentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Comment


class VoteSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Vote
