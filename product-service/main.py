import asyncio

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Product Service")


PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Phone", "price": 50000},
    {"id": 3, "name": "Keyboard", "price": 6000},
]


@app.get("/health")
async def health():
    return {"status": "ok", "service": "product-service"}


@app.get("/products")
async def get_products():
    return PRODUCTS


@app.get("/products/slow")
async def get_products_slow():
    await asyncio.sleep(2)
    return PRODUCTS


@app.get("/products/error")
async def get_products_error():
    raise HTTPException(status_code=500, detail="Test product error")
