import httpx

from app.core.config import settings


class SSOClient:
    async def validate_token(self, authorization: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{settings.SSO_SERVICE_URL}/auth/validate",
                    headers={"Authorization": authorization},
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
