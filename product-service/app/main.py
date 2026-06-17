from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database import Base, engine
from app.infrastructure.models.product_model import ProductModel
from app.presentation.http.product_routes import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="Product Service",
    lifespan=lifespan,
)

app.include_router(product_router)
