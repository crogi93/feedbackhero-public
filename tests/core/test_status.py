from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Board, Status


class StatusTests(APITestCase):
    MOCK_BOARD = {
        "name": "PixelPulse",
        "logo": SimpleUploadedFile(
            name="mock_logo.jpg",
            content=open("tests/images/mock_logo.jpg", "rb").read(),
            content_type="image/jpeg",
        ),
        "description": "Embark on a creative journey with our art application. Immerse yourself in a world of inspiration, connect with artists worldwide, and showcase your masterpieces. Experience the beauty of art wherever you go, only with PixelPulse.",
    }
    MOCK_STATUS = {"name": "Brand new!"}

    def setUp(self) -> None:
        self.board = Board.objects.create(**self.MOCK_BOARD)
        self.status = Status.objects.create(board=self.board, **self.MOCK_STATUS)

    def test_create_status(self) -> None:
        payload = {
            "name": "On going.",
        }
        url = reverse("status-list", kwargs={"bid": 1})
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_get_status_list(self) -> None:
        url = reverse("status-list", kwargs={"bid": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"][0]["name"], self.MOCK_STATUS["name"])

    def test_get_status_detail(self) -> None:
        url = reverse("status-detail", kwargs={"bid": 1, "id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["name"], self.MOCK_STATUS["name"])

    def test_update_status(self) -> None:
        payload = {
            "name": "Released!",
        }
        url = reverse("status-detail", kwargs={"bid": 1, "id": 1})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_delete_status(self) -> None:
        url = reverse("status-detail", kwargs={"bid": 1, "id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
