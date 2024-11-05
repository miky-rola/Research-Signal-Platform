import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpass"
    )

def test_user_view_get_me(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/users/me/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert response.data["username"] == user.username

def test_signup_view_create(api_client):
    data = {
        "email": "new_user@example.com",
        "username": "newuser",
        "password": "newpassword"
    }
    response = api_client.post("/api/signup/", data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "Verification code sent"

def test_logout_view_post(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/logout/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Successfully logged out."

def test_forgot_password_view_create(api_client):
    data = {
        "email": "test@example.com"
    }
    response = api_client.post("/api/forgot-password/", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data

def test_reset_password_view_create(api_client):
    data = {
        "token": "some_valid_token",
        "new_password": "newpassword"
    }
    response = api_client.post("/api/reset-password/", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Password reset successfully"

def test_change_password_view_create(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "old_password": "testpass",
        "new_password": "newpassword"
    }
    response = api_client.post("/api/change-password/", data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Password changed successfully"