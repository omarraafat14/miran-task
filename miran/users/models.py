from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import managers, mixins


class User(mixins.UserMixin, AbstractUser):
    email = models.EmailField(verbose_name="email address", unique=True)
    username = models.CharField(_("username"), max_length=150)
    phone = models.CharField(_("Phone"), max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=10)

    objects = managers.CustomUserManager()
