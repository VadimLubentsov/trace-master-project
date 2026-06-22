import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.infrastructure.cache.redis_provider import get_redis_client
from app.infrastructure.persistence.db_provider import get_engine, get_sessionmaker
from app.presentation.http.product_routes import router as product_router
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

    logger.info("Product service started")

    try:
        yield
    finally:
        await redis_client.aclose()
        await engine.dispose()

        logger.info("Product service stopped")


app = FastAPI(
    title="Product Service",
    lifespan=lifespan,
)

app.middleware("http")(log_http_requests)

app.include_router(product_router)
