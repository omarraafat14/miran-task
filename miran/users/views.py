from . import models
from ..services.views import ModelViewSetClones
from .serializers import (
    LoginSerializer,
    RegisterLoginSerializer,
    UserDataSerializer,
    UserSerializer,
    VerifySerializer,
)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSetClones, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "login":
            return LoginSerializer
        elif self.action in ["update_me", "get_me"]:
            return UserDataSerializer
        elif self.action == "register_login":
            return RegisterLoginSerializer
        elif self.action == "verify":
            return VerifySerializer
        return super().get_serializer_class()

    def get_object(self):
        return self.request.user

    @action(methods=["post"], detail=False, url_path="auth/register")
    def register(self, request, *args, **kwargs):
        return super().create_clone(request, *args, **kwargs)

    @action(methods=["post"], detail=False, url_path="auth/login")
    def login(self, request, *args, **kwargs):
        return super().create_clone(request, data=False, *args, **kwargs)

    @action(methods=["post"], detail=False, url_path="auth/register-login")
    def register_login(self, request, *args, **kwargs):
        return super().create_clone(request, *args, **kwargs)

    @action(methods=["post"], detail=False, url_path="auth/verify")
    def verify(self, request, *args, **kwargs):
        return super().create_clone(request, *args, **kwargs)

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        return super().retrieve_clone(request, *args, **kwargs)

    @me.mapping.patch
    def update_me(self, request, *args, **kwargs):
        return super().partial_update_clone(request, *args, **kwargs)

    @me.mapping.delete
    def delete_me(self, request, *args, **kwargs):
        return super().destroy_clone(request, *args, **kwargs)
