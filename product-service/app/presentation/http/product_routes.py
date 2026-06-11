from fastapi import APIRouter

from app.application.services.product_service import get_all_products
from app.schemas.product import ProductResponse

router = APIRouter(tags=["products"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "product-service"}


@router.get("/products", response_model=list[ProductResponse])
def get_products():
    return get_all_products()
