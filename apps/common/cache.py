import logging
from django_redis.cache import RedisCache

from django.core.cache import cache


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomRedisCache(RedisCache):
    def delete_pattern(self, pattern, version=None):
        """Delete all keys matching the given pattern."""
        pattern = self.make_key(pattern, version=version)
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)

