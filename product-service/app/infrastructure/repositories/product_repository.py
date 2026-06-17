from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.product_model import ProductModel


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[ProductModel]:
        result = await self.db.execute(select(ProductModel).order_by(ProductModel.id))

        return list(result.scalars().all())

    async def create_product(
        self,
        name: str,
        price: int,
        stock_quantity: int,
    ) -> ProductModel:
        product = ProductModel(
            name=name,
            price=price,
            stock_quantity=stock_quantity,
        )

        self.db.add(product)

        return product
