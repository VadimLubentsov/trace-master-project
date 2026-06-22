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
