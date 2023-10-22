from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Board, Comment, Status, Suggestion


class CommentTests(APITestCase):
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
    MOCK_COMMENT = {
        "body": "The enhanced customer engagement features, like the real-time updates and personalized recommendations, made my travel experience smoother and more enjoyable."
    }

    def setUp(self) -> None:
        self.board = Board.objects.create(**self.MOCK_BOARD)
        self.status = Status.objects.create(board=self.board, **self.MOCK_STATUS)
        self.suggestion = Suggestion.objects.create(
            board=self.board, status=self.status, **self.MOCK_SUGGESTION
        )
        self.comment = Comment.objects.create(
            suggestion=self.suggestion, **self.MOCK_COMMENT
        )

    def test_create_comment(self) -> None:
        payload = {
            "body": "Thanks for turning a great trip into an extraordinary one!",
        }
        url = reverse("comment-list", kwargs={"id": 1})
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_get_comment_list(self) -> None:
        url = reverse("comment-list", kwargs={"id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"][0]["body"], self.MOCK_COMMENT["body"])

    def test_get_comment_detail(self) -> None:
        url = reverse("comment-detail", kwargs={"id": 1, "cid": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["body"], self.MOCK_COMMENT["body"])

    def test_update_comment(self) -> None:
        payload = {
            "body": "Awesome idea! I'm looking foward to try it soon.",
        }
        url = reverse("comment-detail", kwargs={"id": 1, "cid": 1})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_delete_comment(self) -> None:
        url = reverse("comment-detail", kwargs={"id": 1, "cid": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
