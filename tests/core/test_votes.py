from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Board, Status, Suggestion, Vote


class VoteTests(APITestCase):
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
        self.comment = Vote.objects.create(suggestion=self.suggestion)

    def test_create_vote(self) -> None:
        url = reverse("vote-list", kwargs={"id": 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["suggestion"])

    def test_get_vote_list(self) -> None:
        url = reverse("vote-list", kwargs={"id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"][0]["suggestion"])

    def test_get_vote_detail(self) -> None:
        url = reverse("vote-detail", kwargs={"id": 1, "cid": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["suggestion"])

    def test_delete_vote(self) -> None:
        url = reverse("vote-detail", kwargs={"id": 1, "cid": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
