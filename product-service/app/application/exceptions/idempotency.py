from app.application.exceptions.base import AppError


class IdempotencyKeyRequiredError(AppError):
    code = "IDEMPOTENCY_KEY_REQUIRED"
    message = "Idempotency-Key header is required"


class IdempotencyConflictError(AppError):
    code = "IDEMPOTENCY_CONFLICT"
    message = "Idempotency key was already used with different request body"


class IdempotencyInProgressError(AppError):
    code = "IDEMPOTENCY_IN_PROGRESS"
    message = "Request with this Idempotency-Key is already processing"
