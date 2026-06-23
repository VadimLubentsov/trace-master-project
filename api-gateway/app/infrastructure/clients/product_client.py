import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class ProductClient:
    async def get_products(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.PRODUCT_SERVICE_URL}/products",
            )

        response.raise_for_status()

        products = response.json()

        logger.info(
            "Product service request completed products_count=%s",
            len(products),
        )

        return products

    async def create_product(
        self,
        product_data: dict,
        idempotency_key: str,
    ) -> dict:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{settings.PRODUCT_SERVICE_URL}/products",
                headers={"Idempotency-Key": idempotency_key},
                json=product_data,
            )

        response.raise_for_status()

        product = response.json()

        logger.info(
            "Product service create request completed product_id=%s name=%s",
            product.get("id"),
            product.get("name"),
        )

        return product
