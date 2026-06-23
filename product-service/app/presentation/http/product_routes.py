import asyncio

from fastapi import APIRouter, Depends, Header, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.idempotency import (
    IdempotencyConflictError,
    IdempotencyInProgressError,
)
from app.application.services.product_service import ProductService
from app.infrastructure.cache.idempotency_repository import IdempotencyRepository
from app.infrastructure.cache.product_cache_repository import ProductCacheRepository
from app.infrastructure.cache.redis_provider import get_redis
from app.infrastructure.persistence.db_provider import get_db
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(tags=["products"])


def get_product_service(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ProductService:
    product_cache_repository = ProductCacheRepository(redis)
    idempotency_repository = IdempotencyRepository(redis)

    return ProductService(
        db=db,
        product_cache_repository=product_cache_repository,
        idempotency_repository=idempotency_repository,
    )


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
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    product_service: ProductService = Depends(get_product_service),
):
    if idempotency_key is None or not idempotency_key.strip():
        raise HTTPException(
            status_code=400,
            detail="Idempotency-Key header is required",
        )

    try:
        return await product_service.create_product(
            name=data.name,
            price=data.price,
            stock_quantity=data.stock_quantity,
            idempotency_key=idempotency_key.strip(),
        )

    except IdempotencyConflictError as err:
        raise HTTPException(
            status_code=409,
            detail="Idempotency key was already used with different request body",
        ) from err

    except IdempotencyInProgressError as err:
        raise HTTPException(
            status_code=409,
            detail="Request with this Idempotency-Key is already processing",
        ) from err


@router.get("/products/slow", response_model=list[ProductResponse])
async def get_products_slow(
    product_service: ProductService = Depends(get_product_service),
):
    await asyncio.sleep(2)

    return await product_service.get_products()


@router.get("/products/error")
async def get_products_error():
    raise HTTPException(status_code=500, detail="Test product error")
