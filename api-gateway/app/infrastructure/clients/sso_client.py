import httpx

from app.core.config import settings


def validate_token(authorization: str) -> dict:
    try:
        response = httpx.post(
            f"{settings.SSO_SERVICE_URL}/auth/validate",
            headers={"Authorization": authorization},
            timeout=5.0,
        )

        response.raise_for_status()

        return response.json()

    except httpx.HTTPStatusError:
        return {
            "valid": False,
            "user_id": None,
            "username": None,
            "role": None,
        }

    except httpx.RequestError:
        return {
            "valid": False,
            "user_id": None,
            "username": None,
            "role": None,
        }
