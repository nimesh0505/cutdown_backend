import logging

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortner.models import ShortenURL
from urlshortner.serialisers import ShortenURLResponseSerialiser, ShortenURLSerialiser

log = logging.getLogger("django")


class HealthCheckView(APIView):
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = "get"

    def get(self, request: Request):
        return Response(
            data={"health_status": "server is running"}, status=status.HTTP_200_OK
        )


class ShortenURLView(APIView):
    serializer_class = ShortenURLSerialiser
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = ("post",)

    @method_decorator(ratelimit(key="ip", rate="10/m", method="POST", block=True))
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.create()
        return Response(
            data=ShortenURLResponseSerialiser({"shorten_url": result.shorten_key}).data,
            status=status.HTTP_201_CREATED,
        )


class RedirectURLView(APIView):
    permission_classes = [
        AllowAny,
    ]
    allowed_methods = ("get",)

    def get(self, request: Request, shorten_key: str):
        instance = ShortenURL.objects.filter(shorten_key=shorten_key).first()
        if not instance:
            return Response(
                data={"message": "Unable to find URL to redirect to"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return HttpResponseRedirect(redirect_to=instance.origin_url)
