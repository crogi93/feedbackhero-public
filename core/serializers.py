from typing import Optional

from rest_framework import serializers

from core.models import Board, Comment, Suggestion, Status, Vote


class BaseSerialzier(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d", required=False, read_only=True
    )
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d", required=False, read_only=True
    )

    class Meta:
        fields = ["id", "created_at", "updated_at"]
        read_only_fields = ["updated_at", "created_at"]


class StatusSerializer(BaseSerialzier):
    class Meta(BaseSerialzier.Meta):
        model = Status
        fields = BaseSerialzier.Meta.fields + ["name", "board"]


class BoardSerializer(BaseSerialzier):
    # status = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    # status = StatusSerializer(many=True, read_only=True)
    logo_url = serializers.SerializerMethodField()

    class Meta(BaseSerialzier.Meta):
        model = Board
        fields = BaseSerialzier.Meta.fields + [
            "name",
            "logo",
            "description",
            "logo_url",
        ]
        read_only_fields = BaseSerialzier.Meta.read_only_fields + ["logo_url"]

    def get_logo_url(self, object: Board) -> Optional[str]:
        if object.logo:
            return object.logo.url
        return None


class SuggestionSerializer(BaseSerialzier):
    comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field="id")
    votes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="id")
    image_url = serializers.SerializerMethodField()

    class Meta(BaseSerialzier.Meta):
        model = Suggestion
        fields = BaseSerialzier.Meta.fields + [
            "board",
            "title",
            "description",
            "comments",
            "image",
            "image_url",
            "author_name",
            "author_email",
            "author_id",
            "status",
            "votes",
        ]
        read_only_fields = BaseSerialzier.Meta.read_only_fields + ["image_url"]

    def get_image_url(self, object: Suggestion) -> Optional[str]:
        if object.image:
            return object.image.url
        return None


class CommentSerializer(BaseSerialzier):
    class Meta(BaseSerialzier.Meta):
        model = Comment
        fields = BaseSerialzier.Meta.fields + [
            "body",
            "author_name",
            "author_id",
            "author_email",
            "suggestion",
            "created_at",
        ]
        read_only_fields = BaseSerialzier.Meta.fields + ["suggestion"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "suggestion"]
