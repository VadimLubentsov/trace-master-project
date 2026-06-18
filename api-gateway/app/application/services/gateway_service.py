import httpx
from fastapi import HTTPException

from app.infrastructure.clients.product_client import ProductClient
from app.infrastructure.clients.sso_client import SSOClient


class GatewayService:
    def __init__(self):
        self.sso_client = SSOClient()
        self.product_client = ProductClient()

    async def get_products_for_authorized_user(
        self,
        authorization: str,
    ) -> list[dict]:
        auth_result = await self.sso_client.validate_token(authorization)

        if not auth_result["valid"]:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
            )

        try:
            return await self.product_client.get_products()

        except httpx.HTTPError as err:
            raise HTTPException(
                status_code=503,
                detail="Product service is unavailable",
            ) from err
