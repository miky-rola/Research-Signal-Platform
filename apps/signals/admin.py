from django.contrib import admin

from .models import MarketData, Signal, UserInteraction


@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = (
        "ticker", 
        "implied_volatility", 
        "historical_volatility", 
        "skew", 
        "created_at"
    )
    list_filter = ("ticker",)
    search_fields = ("ticker",)
    ordering = ("-created_at",)


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = (
        "ticker",
        "strategy",
        "vrp_zscore",
        "vrp_ratio",
        "expected_return",
        "confidence",
        "in_lab",
        "expires_at",
        "created_at"
    )
    list_filter = ("strategy", "in_lab", "expires_at")
    search_fields = ("ticker", "strategy")
    ordering = ("-created_at",)
    date_hierarchy = "expires_at"


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "signal", 
        "status", 
        "position_size", 
        "pnl", 
        "created_at"
    )
    list_filter = ("status", "user")
    search_fields = ("user__username", "signal__ticker")
    ordering = ("-created_at",)
