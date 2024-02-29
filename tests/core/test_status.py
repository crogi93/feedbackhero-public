from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from customers.models import User


class StatusTests(APITestCase):
    fixtures = [
        "tests/core/fixtures/customers.json",
        "tests/core/fixtures/boards.json",
        "tests/core/fixtures/status.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(email="example@proton.me")
        self.token = str(AccessToken.for_user(self.user))
        self.authorization_header = "Bearer {}".format(self.token)
        self.user_2 = User.objects.get(email="example_2@proton.me")
        self.token_2 = str(AccessToken.for_user(self.user_2))
        self.authorization_header_2 = "Bearer {}".format(self.token_2)

    def test_success_post_status(self) -> None:
        url = "/api/boards/1/status"
        payload = {
            "name": "New",
        }
        response = self.client.post(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_unsuccess_post_status(self) -> None:
        url = "/api/boards/1/status"
        payload = {
            "name": "New",
        }
        response = self.client.post(
            url, data=payload, HTTP_AUTHORIZATION=self.authorization_header_2
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success_get_status_list(self) -> None:
        url = "/api/boards/1/status"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"][0]["name"], "Example")

    def test_unauthorized_get_status_list(self) -> None:
        url = "/api/boards/1/status"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_get_status_detail(self) -> None:
        url = "/api/boards/1/status/1"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["name"], "Example")

    def test_success_put_status(self) -> None:
        url = "/api/boards/1/status/1"
        payload = {
            "name": "Released!",
        }
        response = self.client.put(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_success_delete_status(self) -> None:
        url = "/api/boards/1/status/1"
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
