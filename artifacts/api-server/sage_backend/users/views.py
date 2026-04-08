"""
Views for user authentication and profile management.
"""

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import ChangePasswordSerializer, RegisterSerializer, UserProfileSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    POST /api/auth/register
    Body: { username, password }
    Creates a new user + empty profile, returns auth token.
    """
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "username": user.username, "profileComplete": False},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/auth/login
    Body: { username, password }
    Returns auth token and whether the user's profile is complete.
    """
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)
    profile = getattr(user, "profile", None)
    profile_complete = profile.is_complete() if profile else False

    return Response({
        "token": token.key,
        "username": user.username,
        "profileComplete": profile_complete,
    })


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/auth/logout
    Deletes the user's auth token (logs them out).
    """
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({"message": "Logged out successfully."})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    POST /api/auth/change-password
    Body: { current_password, new_password }
    Updates the current user's password.
    """
    serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(serializer.validated_data["new_password"])
    request.user.save(update_fields=["password"])

    Token.objects.filter(user=request.user).delete()
    token = Token.objects.create(user=request.user)

    return Response({
        "message": "Password updated successfully.",
        "token": token.key,
    })


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Current-user CRUD endpoint.

    GET returns the authenticated user's profile.
    PUT fully updates the profile.
    PATCH partially updates the profile.
    DELETE removes the current account and profile.
    """
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "GET":
        serializer = UserProfileSerializer(profile_obj)
        return Response({
            "username": request.user.username,
            "profileComplete": profile_obj.is_complete(),
            **serializer.data,
        })

    if request.method == "DELETE":
        username = request.user.username
        request.user.delete()
        return Response(
            {"message": f"Deleted account for {username}."},
            status=status.HTTP_200_OK,
        )

    serializer = UserProfileSerializer(
        profile_obj,
        data=request.data,
        partial=request.method == "PATCH",
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    profile_obj.refresh_from_db()
    return Response({
        "username": request.user.username,
        "profileComplete": profile_obj.is_complete(),
        **serializer.data,
    })
