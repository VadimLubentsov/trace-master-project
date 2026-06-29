from dataclasses import dataclass

from app.application.enums.idempotency import IdempotencyStatus


@dataclass(frozen=True)
class IdempotencyRecord:
    status: IdempotencyStatus
    request_hash: str
    response_data: dict | None
