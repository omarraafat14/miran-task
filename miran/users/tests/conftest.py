import pytest


@pytest.fixture
def user_sign_up_data():
    return {
        "email": "user@example.com",
        "username": "string",
        "phone": "string",
        "password": "string",
        "password2": "string",
    }


@pytest.fixture
def invalid_user_data():
    return {
        "email": "user@example.com",
        "username": "string",
        "password": "string",
        "password2": "string1",
    }
