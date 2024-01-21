from rest_framework import serializers

from core.models import Board, Comment, Suggestion, Status, Vote


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ["created_at", "deleted_at", "updated_at"]
        fields = "__all__"


class StatusSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Status
        read_only_fields = BaseSerializer.Meta.read_only_fields + ["board"]


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
        read_only_fields = BaseSerializer.Meta.read_only_fields + ["board"]

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
