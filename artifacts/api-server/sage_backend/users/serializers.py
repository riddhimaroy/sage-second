"""
Serializers for user registration, login, and profile management.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_username(self, value):
        if not value.isalnum() and not all(c.isalnum() or c in "_-" for c in value):
            raise serializers.ValidationError("Username may only contain letters, numbers, underscores, and hyphens.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("That username is already taken.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        UserProfile.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError({"new_password": "New password must be different from the current password."})

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "age", "gender", "height_cm", "weight_kg",
            "activity_level", "goal",
            "custom_protein_g", "use_custom_protein",
        ]

    def validate_age(self, value):
        if value is not None and (value < 1 or value > 120):
            raise serializers.ValidationError("Age must be between 1 and 120.")
        return value

    def validate_height_cm(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Height must be a positive number.")
        return value

    def validate_weight_kg(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Weight must be a positive number.")
        return value

    def validate_custom_protein_g(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Protein target must be a positive number.")
        return value
