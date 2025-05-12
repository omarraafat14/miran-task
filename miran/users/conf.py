from django.db import models


class UserTypeChoices(models.TextChoices):
    client = "client", "client"
