from enum import StrEnum


class IdempotencyOperation(StrEnum):
    PRODUCT_CREATE = "products:create"


class IdempotencyStatus(StrEnum):
    PROCESSING = "processing"
    COMPLETED = "completed"
