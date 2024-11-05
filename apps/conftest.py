import pytest
from pytest_factoryboy import register
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.utils import OTPUtils
from apps.users.models import User
from apps.users.tests.factories import (
    UserFactory,
)

register(UserFactory)



@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def test_email():
    return "test@email.com"


@pytest.fixture()
def test_password():
    return "something-a-bit-serious"


@pytest.fixture
def user(test_password) -> User:
    return UserFactory(password=test_password)


@pytest.fixture
def otp_code(user):
    return OTPUtils.generate_otp(user)


@pytest.fixture
def wrong_otp_token():
    return OTPUtils.generate_token("hello")


@pytest.fixture
def token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@pytest.fixture(autouse=True)
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_auth(api_client):
    """
    login user
    """

    def make_auth(user: User):
        api_client.force_authenticate(user=user)
        return api_client

    return make_auth
