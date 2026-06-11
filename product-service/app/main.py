from fastapi import FastAPI

from app.presentation.http.product_routes import router as product_router

app = FastAPI(title="Product Service")

app.include_router(product_router)
