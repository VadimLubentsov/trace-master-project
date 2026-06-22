import json
import logging

from redis.asyncio import Redis

from app.schemas.product import ProductResponse

PRODUCTS_CACHE_KEY = "products:list"
PRODUCTS_CACHE_TTL_SECONDS = 300

logger = logging.getLogger(__name__)


class ProductCacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_products(self) -> list[ProductResponse] | None:
        cached_products = await self.redis.get(PRODUCTS_CACHE_KEY)

        if cached_products is None:
            logger.info("Products cache miss key=%s", PRODUCTS_CACHE_KEY)
            return None

        logger.info("Products cache hit key=%s", PRODUCTS_CACHE_KEY)

        products_data = json.loads(cached_products)

        return [ProductResponse(**product_data) for product_data in products_data]

    async def set_products(self, products: list[ProductResponse]) -> None:
        products_data = [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
            }
            for product in products
        ]

        await self.redis.set(
            PRODUCTS_CACHE_KEY,
            json.dumps(products_data),
            ex=PRODUCTS_CACHE_TTL_SECONDS,
        )

        logger.info(
            "Products cached key=%s count=%s ttl_seconds=%s",
            PRODUCTS_CACHE_KEY,
            len(products),
            PRODUCTS_CACHE_TTL_SECONDS,
        )

    async def delete_products(self) -> None:
        deleted_count = await self.redis.delete(PRODUCTS_CACHE_KEY)

        logger.info(
            "Products cache invalidated key=%s deleted_count=%s",
            PRODUCTS_CACHE_KEY,
            deleted_count,
        )
