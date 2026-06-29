import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.application.exceptions.base import AppError
from app.application.exceptions.idempotency import (
    IdempotencyConflictError,
    IdempotencyInProgressError,
    IdempotencyKeyRequiredError,
)

logger = logging.getLogger(__name__)

APP_ERROR_STATUS_CODES = {
    IdempotencyKeyRequiredError: status.HTTP_400_BAD_REQUEST,
    IdempotencyConflictError: status.HTTP_409_CONFLICT,
    IdempotencyInProgressError: status.HTTP_409_CONFLICT,
}


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    status_code = APP_ERROR_STATUS_CODES.get(
        type(exc),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    logger.info(
        "Application error handled code=%s path=%s status_code=%s",
        exc.code,
        request.url.path,
        status_code,
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unexpected error path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
            }
        },
    )
