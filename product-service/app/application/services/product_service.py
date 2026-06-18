import json

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.product_model import ProductModel
from app.infrastructure.repositories.product_repository import ProductRepository
from app.schemas.product import ProductResponse

PRODUCTS_CACHE_KEY = "products:list"
PRODUCTS_CACHE_TTL_SECONDS = 30


class ProductService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis
        self.product_repository = ProductRepository(db)

    async def get_products(self) -> list[ProductResponse]:
        cached_products = await self.redis.get(PRODUCTS_CACHE_KEY)

        if cached_products is not None:
            products_data = json.loads(cached_products)

            return [ProductResponse(**product_data) for product_data in products_data]

        products = await self.product_repository.get_all()

        response_products = [self._to_response(product) for product in products]

        await self.redis.set(
            PRODUCTS_CACHE_KEY,
            json.dumps(
                [
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "stock_quantity": product.stock_quantity,
                    }
                    for product in response_products
                ]
            ),
            ex=PRODUCTS_CACHE_TTL_SECONDS,
        )

        return response_products

    async def create_product(
        self,
        name: str,
        price: int,
        stock_quantity: int,
    ) -> ProductResponse:
        try:
            product = await self.product_repository.create_product(
                name=name,
                price=price,
                stock_quantity=stock_quantity,
            )

            await self.db.commit()
            await self.db.refresh(product)

            await self.redis.delete(PRODUCTS_CACHE_KEY)

            return self._to_response(product)

        except Exception:
            await self.db.rollback()
            raise

    def _to_response(self, product: ProductModel) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock_quantity=product.stock_quantity,
        )
