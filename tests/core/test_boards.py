from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import pre_save
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Board
from core.signals import auto_delete_file_on_change
from customers.models import User


class BoardTests(APITestCase):
    fixtures = ["tests/core/fixtures/customers.json", "tests/core/fixtures/boards.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(email="example@proton.me")
        self.token = str(AccessToken.for_user(self.user))
        self.authorization_header = "Bearer {}".format(self.token)
        pre_save.disconnect(sender=Board, receiver=auto_delete_file_on_change)

    def test_success_post_board(self) -> None:
        url = "/api/boards"
        payload = {
            "name": "Example Company Name",
            "logo": SimpleUploadedFile(
                name="example_logo.jpg",
                content=open("tests/images/example_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "description": "This is example description 1. This is used for testing purposes",
            "footer": "{'footer_text': 'This is footer text.', 'footer_extra': 'This is extra footer text.', 'contacts': {'twitter': 'www.twitter.com', 'instagram': 'www.instagram.com', 'email': None, 'discord': None, 'website': None}}",
        }

        response = self.client.post(
            url, data=payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        payload.pop("logo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["logo"])
        self.assertTrue(response.json()["data"]["is_active"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_success_get_board_list(self) -> None:
        url = "/api/boards"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["data"])

    def test_unauthorized_get_board_list(self) -> None:
        url = "/api/boards"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_get_board_detail(self) -> None:
        url = "/api/boards/1"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["logo"])
        self.assertEqual(response.json()["data"]["name"], "Example Board 1")
        self.assertEqual(
            response.json()["data"]["description"],
            "This is description for example board 1.",
        )

    def test_success_put_board(self) -> None:
        url = "/api/boards/1"
        payload = {
            "name": "Example Board 3",
            "logo": SimpleUploadedFile(
                name="example_logo.jpg",
                content=open("tests/images/example_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "description": "This is example description 1. This is used for testing purposes",
            "footer": "{'footer_text': 'This is footer text.', 'footer_extra': 'This is extra footer text.', 'contacts': {'twitter': 'www.twitter.com', 'instagram': 'www.instagram.com', 'email': None, 'discord': 'www.discord.com', 'website': None}}",
        }
        response = self.client.put(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        payload.pop("logo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["logo"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_success_delete_board(self) -> None:
        url = "/api/boards/1"
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self) -> None:
        pre_save.connect(sender=Board, receiver=auto_delete_file_on_change)
