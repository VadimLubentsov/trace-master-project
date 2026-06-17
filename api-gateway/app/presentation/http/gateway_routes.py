from fastapi import APIRouter, Depends, Header

from app.application.services.gateway_service import GatewayService

router = APIRouter(tags=["gateway"])


def get_gateway_service() -> GatewayService:
    return GatewayService()


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "api-gateway"}


@router.get("/products")
async def get_products(
    authorization: str = Header(..., alias="Authorization"),
    gateway_service: GatewayService = Depends(get_gateway_service),
):
    return await gateway_service.get_products_for_authorized_user(authorization)
