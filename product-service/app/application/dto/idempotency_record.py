from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyRecord:
    status: str
    request_hash: str
    response_data: dict | None
