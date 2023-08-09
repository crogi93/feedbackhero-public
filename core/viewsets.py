from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import HttpRequest
from rest_framework.views import APIView


class ListView(APIView):
    def get(self, request: HttpRequest) -> JsonResponse:
        objects = self.object_class.objects.all()
        serializer = self.serializer_class(objects, many=True)
        return JsonResponse({"data": serializer.data})

    def post(self, request: HttpRequest) -> JsonResponse:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": self.serializer_class(object).data})


class DetailView(APIView):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(self.object_class, id=id)
        serializer = self.serializer_class(object)
        return JsonResponse({"data": serializer.data})

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(self.object_class, id=id)
        serializer = self.serializer_class(object, data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        object = serializer.save()
        return JsonResponse({"data": self.serializer_class(object).data})

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        object = get_object_or_404(self.object_class, id=id)
        object.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT, safe=False)
