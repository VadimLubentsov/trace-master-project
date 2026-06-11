from fastapi import FastAPI

from app.presentation.http.gateway_routes import router as gateway_router

app = FastAPI(title="API Gateway")

app.include_router(gateway_router)
