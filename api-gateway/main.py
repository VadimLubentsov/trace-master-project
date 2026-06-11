import os
import httpx
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="API Gateway")
SSO_SERVICE_URL = os.getenv("SSO_SERVICE_URL", "http://127.0.0.1:8002")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://127.0.0.1:8001")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "5"))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


async def validate_user(authorization: str | None) -> dict:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.post(
            f"{SSO_SERVICE_URL}/auth/validate",
            headers={"Authorization": authorization or ""},
        )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return response.json()


async def get_products_from_product_service(path: str) -> list[dict]:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}{path}")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Product service error")

    return response.json()


@app.get("/products")
async def get_products(authorization: str | None = Header(default=None)):
    await validate_user(authorization)
    return await get_products_from_product_service("/products")


@app.get("/products/slow")
async def get_products_slow(authorization: str | None = Header(default=None)):
    await validate_user(authorization)
    return await get_products_from_product_service("/products/slow")


@app.get("/products/error")
async def get_products_error(authorization: str | None = Header(default=None)):
    await validate_user(authorization)
    return await get_products_from_product_service("/products/error")
