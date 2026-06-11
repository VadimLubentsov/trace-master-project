from app.domain.entities.product import Product

products = [
    Product(id=1, name="Laptop", price=75000),
    Product(id=2, name="Phone", price=50000),
    Product(id=3, name="Keyboard", price=6000),
]


def get_all_products() -> list[Product]:
    return products
