import httpx

from app.core.config import settings


def get_products() -> list[dict]:
    response = httpx.get(
        f"{settings.PRODUCT_SERVICE_URL}/products",
        timeout=5.0,
    )

    response.raise_for_status()

    return response.json()
