from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.persistence.db_provider import get_engine, get_sessionmaker
from app.presentation.http.product_routes import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    session_factory = get_sessionmaker(engine)

    app.state.engine = engine
    app.state.session_factory = session_factory

    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title="Product Service",
    lifespan=lifespan,
)

app.include_router(product_router)
