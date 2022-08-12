import logging

from django import http
from django_guid import get_guid
from drf_spectacular.utils import extend_schema
from jsonschema import ValidationError
from ratelimit.decorators import ratelimit
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .models import CustomUser
from .serialisers import MessageSerialiser, SignupSerialiser

log = logging.getLogger("django")


@extend_schema(
    summary="Sign Up",
    description="API is used for user to sign up on our platform",
    tags=["Users"],
    responses={201: MessageSerialiser},
)
class SignupView(viewsets.ModelViewSet):
    serializer_class = SignupSerialiser
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ("post",)
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            log.info(f"Started creating user with payload {request.data}")
            response = super().create(request, *args, **kwargs)
            log.info(f"User created with email {response.data['email']}")
            return Response(
                MessageSerialiser(
                    {"message": "your account has been successfully created 😀"}
                ).data,
                status=response.status_code,
            )

        except ValidationError as e:
            return Response(
                MessageSerialiser({"message": e.message}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
