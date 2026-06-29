from fastapi import APIRouter, Depends, Header

from app.application.exceptions.gateway import IdempotencyKeyRequiredError
from app.application.services.gateway_service import GatewayService
from app.schemas.product import ProductCreate

router = APIRouter(tags=["gateway"])


def get_gateway_service() -> GatewayService:
    return GatewayService()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


@router.get("/products")
async def get_products(
    authorization: str = Header(..., alias="Authorization"),
    gateway_service: GatewayService = Depends(get_gateway_service),
):
    return await gateway_service.get_products_for_authorized_user(
        authorization=authorization,
    )


@router.post("/products")
async def create_product(
    data: ProductCreate,
    authorization: str = Header(..., alias="Authorization"),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    gateway_service: GatewayService = Depends(get_gateway_service),
):
    if idempotency_key is None or not idempotency_key.strip():
        raise IdempotencyKeyRequiredError()

    return await gateway_service.create_product_for_authorized_user(
        authorization=authorization,
        product_data=data.model_dump(),
        idempotency_key=idempotency_key.strip(),
    )
