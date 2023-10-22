from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Board, Status, Suggestion


class SuggestionTests(APITestCase):
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
    MOCK_SUGGESTION = {
        "title": "Enhanced Customer Engagement",
        "description": "SkyTravel can improve customer engagement by leveraging technology and social media. Implementing a user-friendly mobile app or website with features such as real-time trip updates, personalized recommendations, and interactive travel blogs can enhance the overall customer experience.",
        "image": SimpleUploadedFile(
            name="mock_logo.jpg",
            content=open("tests/images/mock_logo.jpg", "rb").read(),
            content_type="image/jpeg",
        ),
    }

    def setUp(self) -> None:
        self.board = Board.objects.create(**self.MOCK_BOARD)
        self.status = Status.objects.create(board=self.board, **self.MOCK_STATUS)
        self.suggestion = Suggestion.objects.create(
            board=self.board, status=self.status, **self.MOCK_SUGGESTION
        )

    def test_create_suggestion(self) -> None:
        payload = {
            "title": "Sustainability Initiatives",
            "description": "Incorporating sustainable travel practices can set SkyTravel apart in an increasingly eco-conscious market. This involves partnering with eco-friendly accommodations, promoting responsible tourism, and implementing carbon offset programs.",
            "image": SimpleUploadedFile(
                name="mock_logo.jpg",
                content=open("tests/images/mock_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "status": 1,
        }
        url = reverse("suggestion-list", kwargs={"bid": 1})
        response = self.client.post(url, payload)
        payload.pop("image")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["image"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_get_suggestion_list(self) -> None:
        url = reverse("suggestion-list", kwargs={"bid": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"][0]["image"])
        self.assertEqual(
            response.json()["data"][0]["title"], self.MOCK_SUGGESTION["title"]
        )
        self.assertEqual(
            response.json()["data"][0]["description"],
            self.MOCK_SUGGESTION["description"],
        )

    def test_get_suggestion_detail(self) -> None:
        url = reverse("suggestion-detail", kwargs={"bid": 1, "id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["image"])
        self.assertEqual(
            response.json()["data"]["title"], self.MOCK_SUGGESTION["title"]
        )
        self.assertEqual(
            response.json()["data"]["description"], self.MOCK_SUGGESTION["description"]
        )

    def test_update_suggestion(self) -> None:
        payload = {
            "title": "Personalized Travel Packages",
            "description": "Introduce a more robust and personalized approach to travel packages. Utilize data analytics to understand customer preferences and behavior, allowing SkyTravel to offer tailor-made itineraries.",
            "image": SimpleUploadedFile(
                name="mock_logo.jpg",
                content=open("tests/images/mock_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "status": 1,
        }
        url = reverse("suggestion-detail", kwargs={"bid": 1, "id": 1})
        response = self.client.put(url, payload)
        payload.pop("image")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["image"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_delete_suggestion(self) -> None:
        url = reverse("suggestion-detail", kwargs={"bid": 1, "id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
