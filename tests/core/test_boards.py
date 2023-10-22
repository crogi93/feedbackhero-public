from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Board


class BoardTests(APITestCase):
    MOCK_BOARD = {
        "name": "PixelPulse",
        "logo": SimpleUploadedFile(
            name="mock_logo.jpg",
            content=open("tests/images/mock_logo.jpg", "rb").read(),
            content_type="image/jpeg",
        ),
        "description": "Embark on a creative journey with our art application. Immerse yourself in a world of inspiration, connect with artists worldwide, and showcase your masterpieces. Experience the beauty of art wherever you go, only with PixelPulse.",
    }

    def setUp(self) -> None:
        board = Board.objects.create(**self.MOCK_BOARD)

    def test_create_board(self) -> None:
        payload = {
            "name": "TravelMingle",
            "logo": SimpleUploadedFile(
                name="mock_logo.jpg",
                content=open("tests/images/mock_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "description": "TravelMingle is a cutting-edge travel application designed to enhance your globetrotting experience. It offers real-time flight and hotel bookings",
        }
        url = reverse("board-list")
        response = self.client.post(url, payload)
        payload.pop("logo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["logo"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_get_board_list(self) -> None:
        url = reverse("board-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"][0]["logo"])
        self.assertEqual(response.json()["data"][0]["name"], self.MOCK_BOARD["name"])
        self.assertEqual(
            response.json()["data"][0]["description"], self.MOCK_BOARD["description"]
        )

    def test_get_board_detail(self) -> None:
        url = reverse("board-detail", kwargs={"id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["logo"])
        self.assertEqual(response.json()["data"]["name"], self.MOCK_BOARD["name"])
        self.assertEqual(
            response.json()["data"]["description"], self.MOCK_BOARD["description"]
        )

    def test_update_board(self) -> None:
        payload = {
            "name": "SkyTravel",
            "logo": SimpleUploadedFile(
                name="mock_logo.jpg",
                content=open("tests/images/mock_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "description": "Elevate your journey with bespoke adventures. From exotic escapes to iconic destinations, our expert team crafts seamless, luxurious experiences. Unlock the world's wonders with SkyTravel—where every moment is a masterpiece.",
        }
        url = reverse("board-detail", kwargs={"id": 1})
        response = self.client.put(url, payload)
        payload.pop("logo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["logo"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_delete_board(self) -> None:
        url = reverse("board-detail", kwargs={"id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
