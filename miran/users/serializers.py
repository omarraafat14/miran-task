from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserToken(serializers.Serializer):
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def create_user_token(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return {"refresh_token": str(refresh_token), "access_token": str(access_token)}


class UserSerializer(UserToken, serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password2",
            "phone",
            "refresh_token",
            "access_token",
        ]
        extra_kwargs = {
            "email": {"write_only": True},
            "username": {"write_only": True},
            "password": {"write_only": True},
            "phone": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return self.create_user_token(user)


class LoginSerializer(UserToken, serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        if user := authenticate(email=email, password=password):
            return self.create_user_token(user)
        raise serializers.ValidationError("email or password wrong")


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "phone", "is_new")


class VerifySerializer(UserToken, serializers.Serializer):
    phone = serializers.CharField(write_only=True, default="01111155856")
    otp = serializers.CharField(write_only=True, default=1234)

    def update_user(self, user):
        user.verification_code = None
        user.save()

    def create(self, validated_data):
        user = get_object_or_404(
            User,
            phone=validated_data["phone"],
            verification_code=validated_data["otp"],
        )
        self.update_user(user)
        return self.create_user_token(user)


class RegisterLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone", "is_new")
        read_only_fields = ("is_new",)

    def create(self, validated_data):
        return User.create_user_or_login(validated_data)
