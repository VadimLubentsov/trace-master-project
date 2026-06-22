import hashlib
import logging

from redis.asyncio import Redis

BLACKLIST_TOKEN_PREFIX = "auth:blacklist:"

logger = logging.getLogger(__name__)


class TokenBlacklistRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def add_token(self, token: str, ttl_seconds: int) -> None:
        await self.redis.set(
            self._get_token_key(token),
            "1",
            ex=ttl_seconds,
        )

        logger.info(
            "Token added to blacklist ttl_seconds=%s",
            ttl_seconds,
        )

    async def is_token_blacklisted(self, token: str) -> bool:
        is_blacklisted = bool(await self.redis.exists(self._get_token_key(token)))

        if is_blacklisted:
            logger.info("Token rejected because it is blacklisted")

        return is_blacklisted

    def _get_token_key(self, token: str) -> str:
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        return f"{BLACKLIST_TOKEN_PREFIX}{token_hash}"
