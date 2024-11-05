from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count

from ..common.models import BaseModel as base_model


User = get_user_model()


class MarketData(base_model):
    ticker = models.CharField(max_length=10, db_index=True)
    implied_volatility = models.FloatField()
    historical_volatility = models.FloatField()
    skew = models.FloatField()
    
    class Meta:
        indexes = [
            models.Index(fields=["ticker", "created_at"]),
        ]


class Signal(base_model):
    STRATEGY_CHOICES = [
        ("VRP", "Volatility Risk Premium"),
        ("SKEW", "Volatility Skew"),
        ("TERM", "Term Structure"),
    ]

    ticker = models.CharField(max_length=10, db_index=True)
    strategy = models.CharField(max_length=10, choices=STRATEGY_CHOICES)
    vrp_zscore = models.FloatField()
    vrp_ratio = models.FloatField()
    expected_return = models.FloatField()
    confidence = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    in_lab = models.BooleanField(default=True)
    expires_at = models.DateTimeField()

    def calculate_performance(self):
        taken_signals = self.userinteraction_set.filter(status="taken")
        return taken_signals.aggregate(
            avg_pnl=Avg("pnl"),
            total_trades=Count("id")
        )

    class Meta:
        indexes = [
            models.Index(fields=["ticker", "strategy", "created_at"]),
            models.Index(fields=["is_active", "expires_at"]),
        ]


class UserInteraction(base_model):
    STATUS_CHOICES = [
        ("taken", "Taken"),
        ("watching", "Watching"),
        ("passed", "Passed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    position_size = models.IntegerField(null=True)
    pnl = models.FloatField(null=True)
    exit_price = models.FloatField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "signal", "status"]),
            models.Index(fields=["created_at"]),
        ]
        unique_together = ["user"]