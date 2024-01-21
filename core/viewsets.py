from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import HttpRequest
from rest_framework.views import APIView

from core.models import Board


class ListView(APIView):
    def get(self, request: HttpRequest, bid: int) -> JsonResponse:
        board = get_object_or_404(Board, id=bid)
        objects = self.object_class.objects.filter(board=board)
        serializer = self.serializer_class(objects, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest, bid: int) -> JsonResponse:
        board = get_object_or_404(Board, id=bid)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save(board=board)
        return JsonResponse({"data": self.serializer_class(object).data})


class DetailView(APIView):
    def get(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(Board, id=bid)
        object = get_object_or_404(self.object_class, board=board, id=id)
        serializer = self.serializer_class(object)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(Board, id=bid)
        object = get_object_or_404(self.object_class, board=board, id=id)
        serializer = self.serializer_class(object, data=request.data, partial=True)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save(board=board)
        return JsonResponse({"data": self.serializer_class(object).data})

    def delete(self, request: HttpRequest, bid: int, id: int) -> JsonResponse:
        board = get_object_or_404(Board, id=bid)
        object = get_object_or_404(self.object_class, board=board, id=id)
        object.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)
