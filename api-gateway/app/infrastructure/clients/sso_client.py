import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class SSOClient:
    async def validate_token(self, authorization: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{settings.SSO_SERVICE_URL}/auth/validate",
                    headers={"Authorization": authorization},
                )

            response.raise_for_status()

            auth_result = response.json()

            logger.info(
                "SSO token validation completed valid=%s user_id=%s username=%s",
                auth_result.get("valid"),
                auth_result.get("user_id"),
                auth_result.get("username"),
            )

            return auth_result

        except httpx.HTTPStatusError as err:
            logger.info(
                "SSO token validation rejected status_code=%s",
                err.response.status_code,
            )

            return {
                "valid": False,
                "user_id": None,
                "username": None,
                "role": None,
            }

        except httpx.RequestError:
            logger.exception("SSO service request failed")

            return {
                "valid": False,
                "user_id": None,
                "username": None,
                "role": None,
            }
