from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import pre_save
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from customers.models import User


class CommentTests(APITestCase):
    fixtures = [
        "tests/core/fixtures/customers.json",
        "tests/core/fixtures/boards.json",
        "tests/core/fixtures/status.json",
        "tests/core/fixtures/suggestions.json",
        "tests/core/fixtures/comments.json",
        "tests/core/fixtures/votes.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(email="example@proton.me")
        self.token = str(AccessToken.for_user(self.user))
        self.authorization_header = "Bearer {}".format(self.token)

    def test_success_post_comment(self) -> None:
        url = "/api/boards/1/suggestions/1/comments"
        payload = {
            "body": "This is example commment under suggestion!",
        }
        response = self.client.post(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_success_get_comments_list(self) -> None:
        url = "/api/boards/1/suggestions/1/comments"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"][0]["body"], "Example comments!")

    def test_unauthorized_get_comments_list(self) -> None:
        url = "/api/boards/1/suggestions/1/comments"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comment_detail(self) -> None:
        url = "/api/boards/1/suggestions/1/comments/1"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["body"], "Example comments!")

    def test_update_comment(self) -> None:
        url = "/api/boards/1/suggestions/1/comments/1"
        payload = {
            "body": "This is example comment for suggestion 1.",
        }
        response = self.client.put(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_delete_comment(self) -> None:
        url = "/api/boards/1/suggestions/1/comments/1"
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
