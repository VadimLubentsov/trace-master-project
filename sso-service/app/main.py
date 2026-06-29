import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.exceptions.base import AppError
from app.core.logging_config import setup_logging
from app.infrastructure.cache.redis_provider import get_redis_client
from app.infrastructure.persistence.db_provider import get_engine, get_sessionmaker
from app.presentation.exception_handlers import (
    app_error_handler,
    unexpected_error_handler,
)
from app.presentation.http.auth_routes import router as auth_router
from app.presentation.middlewares.logging_middleware import log_http_requests

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    session_factory = get_sessionmaker(engine)
    redis_client = get_redis_client()

    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.redis = redis_client

    logger.info("SSO service started")

    try:
        yield
    finally:
        await redis_client.aclose()
        await engine.dispose()

        logger.info("SSO service stopped")


app = FastAPI(
    title="SSO Service",
    lifespan=lifespan,
)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

app.middleware("http")(log_http_requests)

app.include_router(auth_router)
