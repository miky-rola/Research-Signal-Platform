from rest_framework import serializers

from .models import (
    MarketData, 
    Signal, 
    UserInteraction
)


class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = [
            "id",
            "ticker",
            "implied_volatility",
            "historical_volatility",
            "skew",
            "created_at",
            "modified_at",
        ]


class SignalSerializer(serializers.ModelSerializer):
    performance = serializers.SerializerMethodField()

    class Meta:
        model = Signal
        fields = [
            "id",
            "ticker",
            "strategy",
            "vrp_zscore",
            "vrp_ratio",
            "expected_return",
            "confidence",
            "in_lab",
            "expires_at",
            "created_at",
            "modified_at",
            "performance",
        ]

    def get_performance(self, obj):
        return obj.calculate_performance


class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = [
            "id",
            "user",
            "signal",
            "status",
            "notes",
            "position_size",
            "pnl",
            "exit_price",
            "created_at",
            "modified_at",
        ]
