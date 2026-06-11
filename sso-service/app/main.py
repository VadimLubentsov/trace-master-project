from fastapi import FastAPI

from app.presentation.http.auth_routes import router as auth_router

app = FastAPI(title="SSO Service")

app.include_router(auth_router)
