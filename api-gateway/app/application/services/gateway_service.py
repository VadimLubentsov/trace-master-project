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

    async def create_product_for_authorized_user(
        self,
        authorization: str,
        product_data: dict,
        idempotency_key: str,
    ) -> dict:
        auth_result = await self.sso_client.validate_token(authorization)

        if not auth_result["valid"]:
            logger.info("Gateway create product rejected reason=invalid_token")

            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
            )

        try:
            product = await self.product_client.create_product(
                product_data=product_data,
                idempotency_key=idempotency_key,
            )

            logger.info(
                "Gateway product create completed user_id=%s username=%s product_id=%s",
                auth_result.get("user_id"),
                auth_result.get("username"),
                product.get("id"),
            )

            return product

        except httpx.HTTPStatusError as err:
            status_code = err.response.status_code

            if status_code == 409:
                logger.info(
                    "Gateway product create rejected "
                    "user_id=%s reason=product_service_conflict",
                    auth_result.get("user_id"),
                )

                detail = err.response.json().get("detail")

                raise HTTPException(
                    status_code=409,
                    detail=detail,
                ) from err

            logger.exception(
                "Gateway product create failed user_id=%s status_code=%s",
                auth_result.get("user_id"),
                status_code,
            )

            raise HTTPException(
                status_code=503,
                detail="Product service is unavailable",
            ) from err

        except httpx.RequestError as err:
            logger.exception(
                "Gateway product create failed "
                "user_id=%s reason=product_service_request_error",
                auth_result.get("user_id"),
            )

            raise HTTPException(
                status_code=503,
                detail="Product service is unavailable",
            ) from err
