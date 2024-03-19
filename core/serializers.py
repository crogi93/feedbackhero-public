from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.models import Board, Comment, Status, Suggestion, Vote


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ["created_at", "deleted_at", "updated_at"]
        fields = "__all__"


class StatusSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Status

    def validate_name(self, value):
        board = self.initial_data.get("board")
        if Status.objects.filter(board=board, name=value).exists():
            raise serializers.ValidationError(
                "A status with this name already exists for this board."
            )
        return value

    def validate_is_default(self, value):
        board_id = self.initial_data.get("board")
        if value:
            if Status.objects.filter(board_id=board_id, is_default=True).exists():
                raise serializers.ValidationError(
                    "A default status already exists for this board."
                )
        return value


class BoardSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Board

    def to_internal_value(self, data):
        if "logo" in data:
            if data["logo"] == "":
                data.pop("logo")
        return super().to_internal_value(data)


class SuggestionSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Suggestion

    def validate_title(self, value):
        board = self.initial_data.get("board")
        if Suggestion.objects.filter(board=board, title=value).exists():
            raise serializers.ValidationError(
                "A status with this name already exists for this board."
            )
        return value

    def to_internal_value(self, data):
        if "image" in data:
            if data["image"] == "":
                data.pop("image")
        return super().to_internal_value(data)


class CommentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Comment
        read_only_fields = BaseSerializer.Meta.read_only_fields + ["suggestion"]


class VoteSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Vote
        read_only_fields = BaseSerializer.Meta.read_only_fields + ["suggestion"]
