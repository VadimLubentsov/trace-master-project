from fastapi import HTTPException

from app.infrastructure.clients.sso_client import validate_token
from app.infrastructure.clients.product_client import get_products


def get_products_for_authorized_user(authorization: str) -> list[dict]:
    auth_result = validate_token(authorization)

    if not auth_result["valid"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    try:
        products = get_products()
        return products

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Product service is unavailable",
        )
