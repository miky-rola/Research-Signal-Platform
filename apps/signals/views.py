from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.core.cache import cache

from .models import (
    MarketData, 
    Signal, 
    UserInteraction
)
from .serializers import (
    MarketDataSerializer, 
    SignalSerializer, 
    UserInteractionSerializer
)
from ..common.paginations import DefaultPagination
from ..common.utils import CustomOrderingFilter


CACHE_TIMEOUT = 60 * 15  # Cache for 15 minutes


class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer
    pagination_class = DefaultPagination

    def perform_create(self, serializer):
        serializer.save()


class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all().prefetch_related("userinteractions")
    serializer_class = SignalSerializer
    pagination_class = DefaultPagination
    filter_backends = [CustomOrderingFilter]


    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to add caching for individual Signal instances.
        """
        instance = self.get_object()
        cache_key = f"signal_{instance.id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, CACHE_TIMEOUT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def perform_create(self, serializer):
        signal = serializer.save()
        cache_key = f"signal_{signal.id}"
        cache.set(cache_key, serializer.data, CACHE_TIMEOUT)

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        signal = self.get_object()
        performance_data = signal.calculate_performance()
        return Response(performance_data, status=status.HTTP_200_OK)


class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all().select_related("user", "signal")
    serializer_class = UserInteractionSerializer
    pagination_class = DefaultPagination
    filter_backends = [CustomOrderingFilter]


    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["get"])
    def user_signals(self, request, pk=None):
        interactions = self.queryset.filter(user_id=pk)
        serializer = self.get_serializer(interactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
