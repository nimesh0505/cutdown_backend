import logging

from django_guid import get_guid
from jsonschema import ValidationError
from rest_framework import serializers

from .models import CustomUser
from .selectors import get_user_by_email

log = logging.getLogger("django")


class MessageSerialiser(serializers.Serializer):
    message = serializers.CharField(required=True)
    trace_id = serializers.CharField(read_only=True, default=get_guid)


class SignupSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "date_of_birth"]

    def validate_email(self, email):
        user = get_user_by_email(email=email)
        if user:
            log.warning(f"user with email {email} already exists")
            raise ValidationError(
                "account with this email already exists. please try different email 😉"
            )
        return email

    def create(self, validated_data):
        validated_data.update(username=validated_data["email"])
        return super().create(validated_data)
