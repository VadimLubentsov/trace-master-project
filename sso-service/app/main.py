from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database import Base
from app.infrastructure.models.user_model import UserModel
from app.infrastructure.persistence.db_provider import get_engine, get_sessionmaker
from app.presentation.http.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    session_factory = get_sessionmaker(engine)

    app.state.engine = engine
    app.state.session_factory = session_factory

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title="SSO Service",
    lifespan=lifespan,
)

app.include_router(auth_router)
