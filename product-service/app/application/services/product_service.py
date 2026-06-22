from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.cache.product_cache_repository import ProductCacheRepository
from app.infrastructure.models.product_model import ProductModel
from app.infrastructure.repositories.product_repository import ProductRepository
from app.schemas.product import ProductResponse


class ProductService:
    def __init__(
        self,
        db: AsyncSession,
        product_cache_repository: ProductCacheRepository,
    ):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.product_cache_repository = product_cache_repository

    async def get_products(self) -> list[ProductResponse]:
        cached_products = await self.product_cache_repository.get_products()

        if cached_products is not None:
            return cached_products

        products = await self.product_repository.get_all()

        response_products = [self._to_response(product) for product in products]

        await self.product_cache_repository.set_products(response_products)

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

            await self.product_cache_repository.delete_products()

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
