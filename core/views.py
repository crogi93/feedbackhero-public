from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.views import APIView

from core.models import Board, Comment, Status, Suggestion, Vote
from core.serializers import (
    BoardSerializer,
    CommentSerializer,
    StatusSerializer,
    SuggestionSerializer,
    VoteSerializer,
)
from core.viewsets import DetailView, ListView


class BoardListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> JsonResponse:
        objects = Board.objects.filter(user=request.user, deleted_at__isnull=True)
        serializer = BoardSerializer(objects, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest) -> JsonResponse:
        data = {**request.data, "user": request.user.id}
        serializer = BoardSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": BoardSerializer(object).data})


class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(
            Board, id=id, user=request.user, deleted_at__isnull=True
        )
        serializer = BoardSerializer(object)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(
            Board, id=id, user=request.user, deleted_at__isnull=True
        )
        serializer = BoardSerializer(object, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": BoardSerializer(object).data})

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(
            Board, id=id, user=request.user, deleted_at__isnull=True
        )
        object.soft_delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)


class StatusListView(ListView):
    object_class = Status
    serializer_class = StatusSerializer


class StatusDetailView(DetailView):
    object_class = Status
    serializer_class = StatusSerializer


class SuggestionListView(ListView):
    object_class = Suggestion
    serializer_class = SuggestionSerializer


class SuggestionDetailView(DetailView):
    object_class = Suggestion
    serializer_class = SuggestionSerializer


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        comments = Comment.objects.filter(suggestion=suggestion)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        comment = serializer.save(suggestion=suggestion)
        return JsonResponse({"data": CommentSerializer(comment).data})


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, bid: int, id: int, cid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        comment = get_object_or_404(Comment, suggestion=suggestion, id=cid)
        serializer = CommentSerializer(comment)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, bid: int, id: int, cid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        comment = get_object_or_404(Comment, suggestion=suggestion, id=cid)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        comment = serializer.save()
        return JsonResponse({"data": CommentSerializer(comment).data})

    def delete(self, request: HttpRequest, bid: int, id: int, cid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        comment = get_object_or_404(Comment, suggestion=suggestion, id=cid)
        comment.soft_delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)


class VoteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        votes = Vote.objects.filter(suggestion=suggestion)
        serializer = VoteSerializer(votes, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        serializer = VoteSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        vote = serializer.save(suggestion=suggestion)
        return JsonResponse({"data": VoteSerializer(vote).data})


class VoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, bid: int, id: int, cid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        vote = get_object_or_404(Vote, suggestion=suggestion, id=cid)
        serializer = VoteSerializer(vote)
        return JsonResponse({"data": serializer.data})

    def delete(self, request: HttpRequest, bid: int, id: int, cid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        suggestion = get_object_or_404(Suggestion, board=board, id=id)
        vote = get_object_or_404(Vote, suggestion=suggestion, id=cid)
        vote.soft_delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)
