from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MarketDataViewSet, 
    SignalViewSet, 
    UserInteractionViewSet
)

router = DefaultRouter()
router.register(r"marketdata", MarketDataViewSet, basename="marketdata")
router.register(r"userinteractions", UserInteractionViewSet, basename="userinteractions")
router.register(r"", SignalViewSet, basename="signals")


urlpatterns = [
    path("", include(router.urls)),
]
