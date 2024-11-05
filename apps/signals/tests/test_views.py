import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token

from ..models import MarketData, Signal, UserInteraction

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )

@pytest.fixture
def auth_client(user):
    client = APIClient()
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client

@pytest.fixture
def market_data():
    return MarketData.objects.create(
        ticker="TXT",
        implied_volatility=0.25,
        historical_volatility=0.20,
        skew=0.10
    )

@pytest.fixture
def signal():
    return Signal.objects.create(
        ticker="TXT",
        strategy="VRP",
        vrp_zscore=1.5,
        vrp_ratio=1.2,
        expected_return=0.15,
        confidence=80,
        in_lab=True,
        expires_at=timezone.now() + timedelta(days=7)
    )

@pytest.fixture
def user_interaction(user, signal):
    return UserInteraction.objects.create(
        user=user,
        signal=signal,
        status="watching",
        position_size=100
    )

@pytest.mark.django_db
class TestMarketDataViewSet:
    def test_list_market_data(self, auth_client, market_data):
        url = reverse("api:marketdata-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["ticker"] == market_data.ticker

    def test_create_market_data(self, auth_client):
        url = reverse("api:marketdata-list")
        data = {
            "ticker": "TEST",
            "implied_volatility": 0.30,
            "historical_volatility": 0.25,
            "skew": 0.15
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert MarketData.objects.count() == 1
        assert MarketData.objects.first().ticker == "TEST"

@pytest.mark.django_db
class TestSignalViewSet:
    def test_list_signals(self, auth_client, signal):
        url = reverse("api:signals-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["ticker"] == signal.ticker

    def test_retrieve_signal_with_cache(self, auth_client, signal):
        url = reverse("api:signals-detail", kwargs={"pk": signal.id})
        
        # First request - should set cache
        response1 = auth_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        
        # Verify cache was set
        cache_key = f"signal_{signal.id}"
        cached_data = cache.get(cache_key)
        assert cached_data is not None
        
        # Second request - should use cache as well
        response2 = auth_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data == response1.data

    def test_create_signal(self, auth_client):
        url = reverse("api:signals-list")
        data = {
            "ticker": "TEST1",
            "strategy": "SKEW",
            "vrp_zscore": 1.8,
            "vrp_ratio": 1.3,
            "expected_return": 0.20,
            "confidence": 85,
            "in_lab": True,
            "expires_at": (timezone.now() + timedelta(days=7)).isoformat()
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Signal.objects.count() == 1
        assert Signal.objects.first().ticker == "TEST1"

    def test_signal_performance(self, auth_client, signal, user_interaction):
        url = reverse("api:signals-performance", kwargs={"pk": signal.id})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "avg_pnl" in response.data
        assert "total_trades" in response.data

    def test_unauthorized_access(self, api_client):
        url = reverse("api:signals-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestUserInteractionViewSet:
    def test_list_user_interactions(self, auth_client, user_interaction):
        url = reverse("api:userinteractions-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == user_interaction.status

    def test_create_user_interaction(self, auth_client, user, signal):
        url = reverse("api:userinteractions-list")
        data = {
            "user": user.id,
            "signal": signal.id,
            "status": "taken",
            "position_size": 200,
            "notes": "Test trade"
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert UserInteraction.objects.count() == 1
        assert UserInteraction.objects.first().position_size == 200

    def test_user_signals_action(self, auth_client, user, user_interaction):
        url = reverse("api:userinteractions-user-signals", kwargs={"pk": user.id})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["status"] == user_interaction.status

    def test_unique_user_signal_constraint(self, auth_client, user_interaction):
        url = reverse("api:userinteractions-list")
        data = {
            "user": user_interaction.user.id,
            "signal": user_interaction.signal.id,
            "status": "taken",
            "position_size": 300
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthorized_access(self, api_client):
        url = reverse("api:userinteractions-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.fixture
def api_client():
    return APIClient()