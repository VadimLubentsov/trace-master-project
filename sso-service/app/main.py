from fastapi import FastAPI

from app.infrastructure.database import Base, engine
from app.infrastructure.models.user_model import UserModel
from app.presentation.http.auth_routes import router as auth_router

app = FastAPI(title="SSO Service")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
