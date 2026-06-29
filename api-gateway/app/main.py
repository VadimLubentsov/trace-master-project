import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.exceptions.base import AppError
from app.core.logging_config import setup_logging
from app.presentation.exception_handlers import (
    app_error_handler,
    unexpected_error_handler,
)
from app.presentation.http.gateway_routes import router as gateway_router
from app.presentation.middlewares.logging_middleware import log_http_requests

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API Gateway started")

    try:
        yield
    finally:
        logger.info("API Gateway stopped")


app = FastAPI(
    title="API Gateway",
    lifespan=lifespan,
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

app.middleware("http")(log_http_requests)

app.include_router(gateway_router)
