import hashlib
import json


class IdempotencyService:
    @staticmethod
    def build_request_hash(data: dict) -> str:
        normalized_data = json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(normalized_data.encode()).hexdigest()
