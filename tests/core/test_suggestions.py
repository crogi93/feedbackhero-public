from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import pre_save
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Suggestion
from core.signals import auto_delete_file_on_change
from customers.models import User


class SuggestionTests(APITestCase):
    fixtures = [
        "tests/core/fixtures/customers.json",
        "tests/core/fixtures/boards.json",
        "tests/core/fixtures/status.json",
        "tests/core/fixtures/suggestions.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(email="example@proton.me")
        self.token = str(AccessToken.for_user(self.user))
        self.authorization_header = "Bearer {}".format(self.token)
        pre_save.disconnect(sender=Suggestion, receiver=auto_delete_file_on_change)

    def test_success_post_suggestion(self) -> None:
        url = "/api/boards/1/suggestions"
        payload = {
            "title": "Suggestion Example!",
            "description": "This is suggestions example description!",
            "image": SimpleUploadedFile(
                name="example_logo.jpg",
                content=open("tests/images/example_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "status": 1,
        }
        response = self.client.post(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        payload.pop("image")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["image"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_success_get_suggestion_list(self) -> None:
        url = "/api/boards/1/suggestions"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"][0]["image"])
        self.assertEqual(response.json()["data"][0]["title"], "Example title")
        self.assertEqual(
            response.json()["data"][0]["description"],
            "Example description!",
        )

    def test_unauthorized_get_suggestion_list(self) -> None:
        url = "/api/boards/1/suggestions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_get_suggestion_detail(self) -> None:
        url = "/api/boards/1/suggestions/1"
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["image"])
        self.assertEqual(response.json()["data"]["title"], "Example title")
        self.assertEqual(
            response.json()["data"]["description"],
            "Example description!",
        )

    def test_success_put_suggestion(self) -> None:
        url = "/api/boards/1/suggestions/1"
        payload = {
            "title": "Example suggestion title!",
            "description": "Introduce a more robust and personalized approach to travel packages. Utilize data analytics to understand customer preferences and behavior, allowing SkyTravel to offer tailor-made itineraries.",
            "image": SimpleUploadedFile(
                name="example_logo.jpg",
                content=open("tests/images/example_logo.jpg", "rb").read(),
                content_type="image/jpeg",
            ),
            "status": 1,
        }
        response = self.client.put(
            url, payload, HTTP_AUTHORIZATION=self.authorization_header
        )
        payload.pop("image")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["image"])
        self.assertDictContainsSubset(payload, response.json()["data"])

    def test_success_delete_suggestion(self) -> None:
        url = "/api/boards/1/suggestions/1"
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.authorization_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self) -> None:
        pre_save.connect(sender=Suggestion, receiver=auto_delete_file_on_change)
