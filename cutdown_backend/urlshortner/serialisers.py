from django.conf import settings
from django_guid import get_guid
from jsonschema import ValidationError
from rest_framework import serializers

from urlshortner.models import ShortenURL


class FreeShortenURLSerialiser(serializers.Serializer):
    origin_url = serializers.CharField(required=True)
    shorten_key = serializers.CharField(read_only=True)

    def create(self):
        origin_url = self.validated_data.get("origin_url")
        instance, _ = ShortenURL.objects.get_or_create(
            origin_url=origin_url, defaults={"origin_url": origin_url}
        )
        return instance


class ShortenURLResponseSerialiser(serializers.Serializer):
    shorten_url = serializers.SerializerMethodField()
    trace_id = serializers.CharField(default=get_guid)

    def get_shorten_url(self, value):
        BASE_URL = settings.BASE_URL
        return f"{BASE_URL}/{value['shorten_url']}"


class NotFoundSerialiser(serializers.Serializer):
    message = serializers.CharField()
    trace_id = serializers.CharField(default=get_guid)


class ShortenURLSerialiser(serializers.Serializer):
    origin_url = serializers.CharField(required=True)
    shorten_key = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(help_text="User ID of the user who is create shorten url")

    def validate_user(self, context, payload):
        if context.get("user_id") != payload.get("user_id"):
            raise ValidationError("user ID is not correct")

    def create(self, context):
        self.validate_user(context, self.validated_data)
        origin_url = self.validated_data.get("origin_url")
        user_id = self.validated_data.get("user_id")
        instance, _ = ShortenURL.objects.get_or_create(
            origin_url=origin_url, user_id=user_id, defaults={"origin_url": origin_url}
        )
        return instance