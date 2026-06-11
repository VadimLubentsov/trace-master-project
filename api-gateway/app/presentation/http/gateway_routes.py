from fastapi import APIRouter, Header

from app.application.services.gateway_service import get_products_for_authorized_user

router = APIRouter(tags=["gateway"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "api-gateway"}


@router.get("/products")
def get_products(authorization: str = Header(...)):
    return get_products_for_authorized_user(authorization)
