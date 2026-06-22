import json

from redis.asyncio import Redis

from app.schemas.product import ProductResponse

PRODUCTS_CACHE_KEY = "products:list"
PRODUCTS_CACHE_TTL_SECONDS = 300


class ProductCacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_products(self) -> list[ProductResponse] | None:
        cached_products = await self.redis.get(PRODUCTS_CACHE_KEY)

        if cached_products is None:
            return None

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

    async def delete_products(self) -> None:
        await self.redis.delete(PRODUCTS_CACHE_KEY)
