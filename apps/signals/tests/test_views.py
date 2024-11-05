import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from datetime import date

from ..models import MarketData, Signal, UserInteraction
from ..serializers import MarketDataSerializer, SignalSerializer, UserInteractionSerializer

User = get_user_model()

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user():
    return User.objects.create_user(email="test@email.com", username="testuser", password="testpass")

@pytest.fixture
def authenticated_api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def market_data():
    return MarketData.objects.create(
        ticker="AAPL",
        implied_volatility=0.2,
        historical_volatility=0.18,
        skew=0.15
    )

@pytest.fixture
def signal(user):
    return Signal.objects.create(
        ticker="AAPL",
        strategy="VRP",
        vrp_zscore=1.2,
        vrp_ratio=0.8,
        expected_return=0.05,
        confidence=90,
        in_lab=True,
        expires_at="2019-08-24T14:15:22Z",
    )

@pytest.fixture
def user_interaction(signal, user):
    return UserInteraction.objects.create(
        user=user,
        signal=signal,
        status="taken",
        position_size=100,
        pnl=500.0,
        exit_price=50.5
    )

@pytest.mark.django_db
def test_market_data_list(authenticated_api_client, market_data):
    url = reverse("api:marketdata-list")
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0] == MarketDataSerializer(market_data).data


@pytest.mark.django_db
def test_signal_list(authenticated_api_client, signal):
    url = reverse("api:signals-list")
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0] == SignalSerializer(signal).data

# @pytest.mark.django_db
# def test_signal_retrieve(authenticated_api_client, signal):
#     url = reverse("api:signals-detail", args=[signal.id])
#     response = authenticated_api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data == SignalSerializer(signal).data

# @pytest.mark.django_db
# def test_user_interaction_list(authenticated_api_client, user_interaction):
#     url = reverse("api:userinteractions-list")
#     response = authenticated_api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data["results"]) == 1
#     assert response.data["results"][0] == UserInteractionSerializer(user_interaction).data

# @pytest.mark.django_db
# def test_user_interaction_create(authenticated_api_client, signal, user):
#     url = reverse("api:userinteractions-list")
#     data = {
#         "user": user.id,
#         "signal": signal.id,
#         "status": "taken",
#         "position_size": 100,
#         "pnl": 500.0
#     }
#     response = authenticated_api_client.post(url, data, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#     assert UserInteraction.objects.count() == 1