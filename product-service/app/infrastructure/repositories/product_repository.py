from sqlalchemy.orm import Session

from app.infrastructure.models.product_model import ProductModel


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ProductModel]:
        return self.db.query(ProductModel).order_by(ProductModel.id).all()

    def create_product(
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
        self.db.commit()
        self.db.refresh(product)

        return product
