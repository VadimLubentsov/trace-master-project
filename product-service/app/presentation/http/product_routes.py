import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.product_service import ProductService
from app.infrastructure.database import get_db
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(tags=["products"])


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/health")
async def health():
    return {"status": "ok", "service": "product-service"}


@router.get("/products", response_model=list[ProductResponse])
async def get_products(
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_products()


@router.post("/products", response_model=ProductResponse)
async def create_product(
    data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_product(
        name=data.name,
        price=data.price,
        stock_quantity=data.stock_quantity,
    )


@router.get("/products/slow", response_model=list[ProductResponse])
async def get_products_slow(
    product_service: ProductService = Depends(get_product_service),
):
    await asyncio.sleep(2)

    return await product_service.get_products()


@router.get("/products/error")
async def get_products_error():
    raise HTTPException(status_code=500, detail="Test product error")
