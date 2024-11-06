import pytest
from django.core import mail
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User


pytestmark = pytest.mark.django_db


class TestUserView:
    def test_user_list(self, api_client_auth, user: User):
        url = reverse("api:users-list")
        client = api_client_auth(user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert "results" in resp_data

    def test_user_read(self, api_client_auth, user: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["email"] == user.email

    def test_user_update(self, api_client_auth, user: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(user)
        data = {"email": "testemail@a.com", "username": "hello_world"}

        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["username"] == data["username"]
        assert resp_data["email"] == data["email"]

    def test_me(
        self,
        api_client_auth,
        user: User,
    ):
        url = reverse("api:users-me")
        client = api_client_auth(user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["email"] == user.email


class TestAuthView:
    def test_login(self, api_client: APIClient, user: User, test_password):
        url = reverse("api:token-obtain")
        response = api_client.post(
            url, data={"email": user.email, "password": test_password}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_login_with_wrong_credentials(
        self, api_client: APIClient, user: User, test_password
    ):
        url = reverse("api:token-obtain")
        response = api_client.post(
            url, data={"email": user.email, "password": "wrong_password"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_signup(self, api_client: APIClient, test_password, test_email):
        url = reverse("api:signup")
        data = {
            "email": test_email,
            "username": "test_name",
            "password": test_password,
            "password2": test_password,
        }
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED

        assert len(mail.outbox) == 0

    def test_refresh_token(self, api_client: APIClient, user: User, token: dict):
        url = reverse("api:token-refresh")

        data = {"refresh": token["refresh"]}
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_200_OK

    def test_change_password(self, api_client_auth, user, test_password):
        url = reverse("api:change-password")
        client = api_client_auth(user=user)
        data = {"old_password": test_password, "new_password": "new_password"}
        resp = client.post(url, data=data)

        assert resp.status_code == status.HTTP_200_OK

    def test_change_password_wrong_password(self, api_client_auth, user, test_password):
        url = reverse("api:change-password")
        client = api_client_auth(user=user)
        data = {"old_password": "wrong_password", "new_password": "new_password"}
        resp = client.post(url, data=data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_forget_password(self, api_client, user):
        url = reverse("api:forget-password")

        resp = api_client.post(url, data={"email": user.email})
        resp_data = resp.json()
        print(resp_data)

        assert resp.status_code == status.HTTP_200_OK
        assert "token" in resp_data

    def test_forget_password_wrong_email(self, api_client, user):
        url = reverse("api:forget-password")

        resp = api_client.post(url, data={"email": "mikyrola8@gmail.com"})
        resp_data = resp.json()
        print(resp_data)

        assert resp.status_code == status.HTTP_200_OK
        assert "token" in resp_data

    def test_reset_password(self, api_client, otp_code, test_password):
        code, token = otp_code
        url = reverse("api:reset-password")
        data = {"token": token, "code": code, "password": test_password}
        resp = api_client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert "message" in resp_data

    def test_reset_password_wrong_code(self, api_client, otp_code, test_password):
        _, token = otp_code
        url = reverse("api:reset-password")
        data = {"token": token, "code": "000000", "password": test_password}
        resp = api_client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid code" in resp_data

    def test_reset_password_wrong_token(
        self, api_client, otp_code, wrong_otp_token, test_password
    ):
        code, _ = otp_code
        url = reverse("api:reset-password")
        data = {"token": wrong_otp_token, "code": code, "password": test_password}
        resp = api_client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid token" in resp_data