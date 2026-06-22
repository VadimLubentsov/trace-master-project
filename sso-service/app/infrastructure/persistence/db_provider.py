import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower() in ("1", "true", "yes", "on")


SQLALCHEMY_ECHO = get_bool_env("SQLALCHEMY_ECHO", default=False)


def get_engine() -> AsyncEngine:
    return create_async_engine(
        DATABASE_URL,
        echo=SQLALCHEMY_ECHO,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )


def get_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_factory = request.app.state.session_factory

    async with session_factory() as session:
        yield session
