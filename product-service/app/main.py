from fastapi import FastAPI

from app.infrastructure.database import Base, engine
from app.infrastructure.models.product_model import ProductModel
from app.presentation.http.product_routes import router as product_router

app = FastAPI(title="Product Service")

Base.metadata.create_all(bind=engine)

app.include_router(product_router)
