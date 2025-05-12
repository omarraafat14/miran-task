from typing import Any, Sequence

from django.contrib.auth import get_user_model

from ...addonsapp.factories import CountryFactory, RegionFactory
from factory import Faker, post_generation
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register  # Registers as pytest fixture
class UserFactory(DjangoModelFactory):
    username = Faker("user_name")  # Generate random username
    email = Faker("email")  # Generate random email

    @post_generation  # Run after instance creation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        # Use provided password or generate one
        password = (
            extracted
            if extracted
            else Faker("password").evaluate(
                None,
                None,
                extra={
                    "locale": "en_US",
                    "length": 12,
                    "special_chars": True,
                    "digits": True,
                    "upper_case": True,
                    "lower_case": True,
                },
            )
        )
        # Hash the password properly
        self.set_password(password)
        self.save()

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]  # Avoid duplicates
        skip_postgeneration_save = True
