import logging

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django_guid import get_guid
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortner.models import ShortenURL
from urlshortner.serialisers import (
    FreeShortenURLSerialiser,
    NotFoundSerialiser,
    ShortenURLResponseSerialiser,
    ShortenURLSerialiser,
)

log = logging.getLogger(__name__)


@extend_schema(
    summary="Server Health",
    description="This is used to check the server health",
    tags=["Server Health Check"],
)
class HealthCheckView(APIView):
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = ("get",)

    def get(self, request: Request):
        return Response(
            data={"message": "server is running"}, status=status.HTTP_200_OK
        )


@extend_schema(
    summary="URL Shortner",
    description="This API is used for shortning the URL and it free. This has rate limitter",
    tags=["URL Shortner"],
    request=ShortenURLSerialiser,
    responses={201: ShortenURLResponseSerialiser},
)
class FreeShortenURLView(APIView):
    serializer_class = FreeShortenURLSerialiser
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = ("post",)

    @method_decorator(ratelimit(key="ip", rate="10/m", block=True))
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.create()
        return Response(
            data=ShortenURLResponseSerialiser({"shorten_url": result.shorten_key}).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    summary="URL Shortner",
    description="This API is used for shortning the URL for user who are registered on our platform",
    tags=["URL Shortner"],
    request=ShortenURLSerialiser,
    responses={201: ShortenURLResponseSerialiser},
)
class ShortenURLView(APIView):
    serializer_class = ShortenURLSerialiser
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = ("post",)

    def post(self, request: Request):
        user_id = request.user.id
        serializer = self.serializer_class(
            data=request.data, context={"user_id": user_id}
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.create()
        return Response(
            data=ShortenURLResponseSerialiser({"shorten_url": result.shorten_key}).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    summary="Redirect API",
    description="API is used for redirecting to target URL",
    tags=["Redirect"],
    exclude=False,
)
class RedirectURLView(APIView):
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = ("get",)

    def get(self, request: Request, cutdown_url: str):
        clients_ip = request.META.get("REMOTE_ADDR")
        log.info(f"CLIENT IP {clients_ip}")

        instance = ShortenURL.objects.filter(shorten_key=cutdown_url).first()
        if not instance:
            log.info(f"shorten key {cutdown_url} not found")
            return Response(
                data=NotFoundSerialiser(
                    {
                        "message": "Unable to find URL to redirect to",
                        "trace_id": get_guid(),
                    }
                ).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        return HttpResponseRedirect(redirect_to=instance.origin_url)
