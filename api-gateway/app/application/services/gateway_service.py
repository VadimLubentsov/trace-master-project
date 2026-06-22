import logging

import httpx
from fastapi import HTTPException

from app.infrastructure.clients.product_client import ProductClient
from app.infrastructure.clients.sso_client import SSOClient

logger = logging.getLogger(__name__)


class GatewayService:
    def __init__(self):
        self.sso_client = SSOClient()
        self.product_client = ProductClient()

    async def get_products_for_authorized_user(
        self,
        authorization: str,
    ) -> list[dict]:
        auth_result = await self.sso_client.validate_token(authorization)

        if not auth_result["valid"]:
            logger.info("Gateway request rejected reason=invalid_token")

            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
            )

        try:
            products = await self.product_client.get_products()

            logger.info(
                "Gateway products request completed "
                "user_id=%s username=%s products_count=%s",
                auth_result.get("user_id"),
                auth_result.get("username"),
                len(products),
            )

            return products

        except httpx.HTTPError as err:
            logger.exception(
                "Gateway products request failed "
                "user_id=%s reason=product_service_unavailable",
                auth_result.get("user_id"),
            )

            raise HTTPException(
                status_code=503,
                detail="Product service is unavailable",
            ) from err
