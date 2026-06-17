from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database import Base, engine
from app.infrastructure.models.user_model import UserModel
from app.presentation.http.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="SSO Service",
    lifespan=lifespan,
)

app.include_router(auth_router)
