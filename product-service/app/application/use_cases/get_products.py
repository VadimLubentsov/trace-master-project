from sqlalchemy.orm import Session

from app.infrastructure.repositories.product_repository import ProductRepository


def get_products(db: Session):
    product_repository = ProductRepository(db)

    return product_repository.get_all()
