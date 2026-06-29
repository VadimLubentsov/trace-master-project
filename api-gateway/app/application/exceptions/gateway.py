from app.application.exceptions.base import AppError


class InvalidTokenError(AppError):
    code = "INVALID_TOKEN"
    message = "Invalid or expired token"


class IdempotencyKeyRequiredError(AppError):
    code = "IDEMPOTENCY_KEY_REQUIRED"
    message = "Idempotency-Key header is required"


class ProductServiceUnavailableError(AppError):
    code = "PRODUCT_SERVICE_UNAVAILABLE"
    message = "Product service is unavailable"


class ProductServiceConflictError(AppError):
    code = "PRODUCT_SERVICE_CONFLICT"
    message = "Product service conflict"
