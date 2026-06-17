from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.auth_service import AuthService
from app.infrastructure.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    ValidateTokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "sso-service"}


@router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.register_user(
        username=data.username,
        password=data.password,
        role=data.role,
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = await auth_service.login_user(
        username=data.username,
        password=data.password,
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return token


@router.post("/validate", response_model=ValidateTokenResponse)
async def validate(
    authorization: str = Header(..., alias="Authorization"),
    auth_service: AuthService = Depends(get_auth_service),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    token = authorization.replace("Bearer ", "")

    result = auth_service.validate_token(token)

    if not result.valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return result
