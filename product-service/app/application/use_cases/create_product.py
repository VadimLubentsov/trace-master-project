from sqlalchemy.orm import Session

from app.infrastructure.repositories.product_repository import ProductRepository


def create_product(
    db: Session,
    name: str,
    price: int,
    stock_quantity: int,
):
    product_repository = ProductRepository(db)

    return product_repository.create_product(
        name=name,
        price=price,
        stock_quantity=stock_quantity,
    )
