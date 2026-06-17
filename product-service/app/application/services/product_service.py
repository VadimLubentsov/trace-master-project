from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.product_model import ProductModel
from app.infrastructure.repositories.product_repository import ProductRepository
from app.schemas.product import ProductResponse


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repository = ProductRepository(db)

    async def get_products(self) -> list[ProductResponse]:
        products = await self.product_repository.get_all()

        return [self._to_response(product) for product in products]

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
