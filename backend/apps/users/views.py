from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


def error_response(status_code, error, message):
    return Response(
        {
            "status": status_code,
            "error": error,
            "message": message,
        },
        status=status_code,
    )


def token_expires_in():
    return int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return error_response(
            status.HTTP_400_BAD_REQUEST,
            "Bad Request",
            "Email y password son obligatorios",
        )
    user = authenticate(request, username=email, password=password)
    if user is None:
        return error_response(
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
            "Credenciales invalidas",
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "expires_in": token_expires_in(),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token_value = request.data.get("refresh_token")
    if not refresh_token_value:
        return error_response(
            status.HTTP_400_BAD_REQUEST,
            "Bad Request",
            "refresh_token es obligatorio",
        )
    try:
        refresh = RefreshToken(refresh_token_value)
    except TokenError:
        return error_response(
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
            "refresh_token invalido o expirado",
        )
    return Response(
        {
            "access_token": str(refresh.access_token),
            "expires_in": token_expires_in(),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def logout(request):
    refresh_token_value = request.data.get("refresh_token")
    if not refresh_token_value:
        return error_response(
            status.HTTP_400_BAD_REQUEST,
            "Bad Request",
            "refresh_token es obligatorio",
        )
    try:
        refresh = RefreshToken(refresh_token_value)
        refresh.blacklist()
    except TokenError:
        return error_response(
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
            "refresh_token invalido o ya fue invalidado",
        )
    return Response(status=status.HTTP_204_NO_CONTENT)
