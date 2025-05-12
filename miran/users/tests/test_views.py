from django.core import mail
from django.urls import reverse

import pytest


pytestmark = pytest.mark.django_db


class TestUserView:
    @pytest.mark.parametrize(
        "user_data,expected_status",
        [
            ("user_sign_up_data", 201),
            ("invalid_user_data", 400),
        ],
    )
    def test_register(self, api_client, user_data, expected_status, request):
        # Arrange
        url = reverse("users-register")
        data = request.getfixturevalue(user_data)
        # Act
        resp = api_client.post(url, data)
        # Assert
        print(resp.json())
        assert resp.status_code == expected_status

    @pytest.mark.parametrize(
        "client,expected_status",
        [
            ("api_client", 401),
            ("api_client_with_credentials", 200),
        ],
    )
    def test_login(self, api_client, user_data, expected_status, request):
        # Arrange
        url = reverse("users-login")
        data = request.getfixturevalue(user_data)
        # Act
        resp = api_client.post(url, data)
        # Assert
        assert resp.status_code == expected_status
