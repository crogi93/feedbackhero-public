from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
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


class BoardListView(ListView):
    def get(self, request: HttpRequest) -> JsonResponse:
        objects = Board.objects.all()
        serializer = BoardSerializer(objects, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest) -> JsonResponse:
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": BoardSerializer(object).data})


class BoardDetailView(DetailView):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(Board, id=id)
        serializer = BoardSerializer(object)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(Board, id=id)
        serializer = BoardSerializer(object, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": BoardSerializer(object).data})

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(Board, id=id)
        object.delete()
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
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        comments = Comment.objects.filter(suggestion=suggestion)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest, id: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        comment = serializer.save(suggestion=suggestion)
        return JsonResponse({"data": CommentSerializer(comment).data})


class CommentDetailView(APIView):
    def get(self, request: HttpRequest, id: int, cid: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        comment = get_object_or_404(Comment, suggestion=suggestion, id=cid)
        serializer = CommentSerializer(comment)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, id: int, cid: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        comment = get_object_or_404(Comment, suggestion=suggestion, id=cid)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        comment = serializer.save()
        return JsonResponse({"data": CommentSerializer(comment).data})

    def delete(self, request: HttpRequest, id: int, cid: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        comment = get_object_or_404(Comment, suggestion=suggestion, id=cid)
        comment.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)


class VoteListView(APIView):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        votes = Vote.objects.filter(suggestion=suggestion)
        serializer = VoteSerializer(votes, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest, id: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        serializer = VoteSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        vote = serializer.save(suggestion=suggestion)
        return JsonResponse({"data": VoteSerializer(vote).data})


class VoteDetailView(APIView):
    def get(self, request: HttpRequest, id: int, cid: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        vote = get_object_or_404(Vote, suggestion=suggestion, id=cid)
        serializer = VoteSerializer(vote)
        return JsonResponse({"data": serializer.data})

    def delete(self, request: HttpRequest, id: int, cid: int) -> JsonResponse:
        suggestion = get_object_or_404(Suggestion, id=id)
        vote = get_object_or_404(Vote, suggestion=suggestion, id=cid)
        vote.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)
