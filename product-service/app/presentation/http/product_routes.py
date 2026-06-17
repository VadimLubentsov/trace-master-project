import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.use_cases.create_product import (
    create_product as create_product_use_case,
)
from app.application.use_cases.get_products import get_products as get_products_use_case
from app.infrastructure.database import get_db
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(tags=["products"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "product-service"}


@router.get("/products", response_model=list[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    products = get_products_use_case(db=db)

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock_quantity=product.stock_quantity,
        )
        for product in products
    ]


@router.post("/products", response_model=ProductResponse)
async def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = create_product_use_case(
        db=db,
        name=data.name,
        price=data.price,
        stock_quantity=data.stock_quantity,
    )

    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        stock_quantity=product.stock_quantity,
    )


@router.get("/products/slow", response_model=list[ProductResponse])
async def get_products_slow(db: Session = Depends(get_db)):
    await asyncio.sleep(2)

    products = get_products_use_case(db=db)

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock_quantity=product.stock_quantity,
        )
        for product in products
    ]


@router.get("/products/error")
async def get_products_error():
    raise HTTPException(status_code=500, detail="Test product error")
