from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.cache.redis_provider import get_redis_client
from app.infrastructure.persistence.db_provider import get_engine, get_sessionmaker
from app.presentation.http.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    session_factory = get_sessionmaker(engine)
    redis_client = get_redis_client()

    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.redis = redis_client

    try:
        yield
    finally:
        await redis_client.aclose()
        await engine.dispose()


app = FastAPI(
    title="SSO Service",
    lifespan=lifespan,
)

app.include_router(auth_router)
