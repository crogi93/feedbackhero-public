from rest_framework import serializers

from core.models import Board, Comment, Suggestion, Status, Vote


class BoardSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(many=True, read_only=True, slug_field="id")

    class Meta:
        model = Board
        fields = ["id", "name", "logo", "description", "status"]
        read_only_fields = ["created_at", "updated_at"]


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name", "board"]
        read_only_fields = ["created_at", "updated_at"]


class SuggestionSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field="id")
    votes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="id")

    class Meta:
        model = Suggestion
        fields = [
            "id",
            "title",
            "image",
            "description",
            "author_name",
            "author_id",
            "author_email",
            "status",
            "created_at",
            "updated_at",
            "comments",
            "board",
            "votes",
        ]
        read_only_fields = ["created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "body",
            "author_name",
            "author_id",
            "author_email",
            "suggestion",
            "created_at",
        ]
        read_only_fields = ["suggestion", "created_at", "updated_at"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "suggestion"]
