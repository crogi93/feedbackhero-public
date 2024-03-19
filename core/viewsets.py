from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.views import APIView

from core.models import Board


class ListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, bid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        objects = self.object_class.objects.filter(board=board)
        serializer = self.serializer_class(objects, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest, bid: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        serializer = self.serializer_class(data={**request.data, "board": bid})
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        object = serializer.save()
        return JsonResponse({"data": self.serializer_class(object).data})


class DetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        object = get_object_or_404(self.object_class, board=board, id=id)
        serializer = self.serializer_class(object)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(
            Board, id=bid, user=request.user, deleted_at__isnull=True
        )
        object = get_object_or_404(self.object_class, board=board, id=id)
        serializer = self.serializer_class(object, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": self.serializer_class(object).data})

    def delete(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(Board, id=bid)
        object = get_object_or_404(self.object_class, board=board, id=id)
        object.soft_delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)
