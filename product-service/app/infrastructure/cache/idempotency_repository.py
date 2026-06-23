import hashlib
import json
import logging

from redis.asyncio import Redis

from app.application.dto.idempotency_record import IdempotencyRecord

IDEMPOTENCY_KEY_PREFIX = "idempotency"
IDEMPOTENCY_TTL_SECONDS = 60 * 60 * 24

logger = logging.getLogger(__name__)


class IdempotencyRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_record(
        self,
        operation: str,
        idempotency_key: str,
    ) -> IdempotencyRecord | None:
        redis_key = self._get_redis_key(operation, idempotency_key)

        raw_record = await self.redis.get(redis_key)

        if raw_record is None:
            logger.info("Idempotency record miss operation=%s", operation)
            return None

        record_data = json.loads(raw_record)

        logger.info(
            "Idempotency record found operation=%s status=%s",
            operation,
            record_data["status"],
        )

        return IdempotencyRecord(
            status=record_data["status"],
            request_hash=record_data["request_hash"],
            response_data=record_data.get("response_data"),
        )

    async def reserve_operation(
        self,
        operation: str,
        idempotency_key: str,
        request_hash: str,
    ) -> bool:
        redis_key = self._get_redis_key(operation, idempotency_key)

        record_data = {
            "status": "processing",
            "request_hash": request_hash,
            "response_data": None,
        }

        was_reserved = await self.redis.set(
            redis_key,
            json.dumps(record_data),
            ex=IDEMPOTENCY_TTL_SECONDS,
            nx=True,
        )

        logger.info(
            "Idempotency operation reserved operation=%s reserved=%s",
            operation,
            bool(was_reserved),
        )

        return bool(was_reserved)

    async def save_completed_response(
        self,
        operation: str,
        idempotency_key: str,
        request_hash: str,
        response_data: dict,
    ) -> None:
        redis_key = self._get_redis_key(operation, idempotency_key)

        record_data = {
            "status": "completed",
            "request_hash": request_hash,
            "response_data": response_data,
        }

        await self.redis.set(
            redis_key,
            json.dumps(record_data),
            ex=IDEMPOTENCY_TTL_SECONDS,
        )

        logger.info(
            "Idempotency response saved operation=%s ttl_seconds=%s",
            operation,
            IDEMPOTENCY_TTL_SECONDS,
        )

    async def delete_record(
        self,
        operation: str,
        idempotency_key: str,
    ) -> None:
        redis_key = self._get_redis_key(operation, idempotency_key)

        deleted_count = await self.redis.delete(redis_key)

        logger.info(
            "Idempotency record deleted operation=%s deleted_count=%s",
            operation,
            deleted_count,
        )

    def _get_redis_key(self, operation: str, idempotency_key: str) -> str:
        key_hash = hashlib.sha256(idempotency_key.encode()).hexdigest()

        return f"{IDEMPOTENCY_KEY_PREFIX}:{operation}:{key_hash}"
