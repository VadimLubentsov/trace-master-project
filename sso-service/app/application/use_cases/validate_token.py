from app.infrastructure.security.jwt_service import decode_access_token


def validate_token(token: str) -> dict:
    payload = decode_access_token(token)

    if payload is None:
        return {
            "valid": False,
            "user_id": None,
            "username": None,
            "role": None,
        }

    return {
        "valid": True,
        "user_id": payload.get("user_id"),
        "username": payload.get("sub"),
        "role": payload.get("role"),
    }
