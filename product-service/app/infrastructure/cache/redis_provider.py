import os

from dotenv import load_dotenv
from fastapi import Request
from redis.asyncio import Redis

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis_client() -> Redis:
    return Redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
