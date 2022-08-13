import logging

from drf_spectacular.utils import extend_schema
from jsonschema import ValidationError
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serialisers import MessageSerialiser, SignInSerialiser, SignupSerialiser

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


@extend_schema(
    summary="Sign In",
    description="API is used for user to sign in our platform",
    tags=["Users"],
    request=SignInSerialiser,
)
class SignInView(viewsets.ModelViewSet):
    serializer_class = SignInSerialiser
    permission_classes = (AllowAny,)
    http_method_names = ("post",)
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serialisers = self.serializer_class(data=request.data)
        serialisers.is_valid(raise_exception=True)
        validated_data = serialisers.validated_data
        validated_data["username"] = validated_data["email"]
        from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

        auth_serializer = TokenObtainPairSerializer(data=validated_data)
        auth_serializer.is_valid(raise_exception=True)

        return auth_serializer.validated_data
