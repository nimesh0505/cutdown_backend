from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from urlshortner.models import ShortenURL

client = APIClient()


class TestShortenURLModel(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_should_create_record_with_shorten_key(self):
        origin_url = "https://www.example.com"
        instance = ShortenURL.objects.create(origin_url=origin_url)

        self.assertEqual(instance.origin_url, origin_url)
        self.assertEqual(len(instance.shorten_key), 8)


class TestShortenURLCreation(APITestCase):
    def setUp(self) -> None:
        self.origin_url = "https://www.example.com"
        return super().setUp()

    def test_should_successfully_return_shorten_url(self):

        response = client.post(reverse("shorten_url"), {"origin_url": self.origin_url})
        response_body = response.json()

        instance = ShortenURL.objects.get(origin_url=self.origin_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_body,
            {"shorten_url": f"{settings.BASE_URL}/{instance.shorten_key}"},
        )

    def test_should_duplicate_origin_url(self):

        for _ in range(3):
            client.post(reverse("shorten_url"), {"origin_url": self.origin_url})
        total_records = ShortenURL.objects.all().count()

        self.assertEqual(total_records, 1)
