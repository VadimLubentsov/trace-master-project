from fastapi import APIRouter, Depends, Header
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.auth import InvalidTokenError, TokenRequiredError
from app.application.services.auth_service import AuthService
from app.infrastructure.cache.redis_provider import get_redis
from app.infrastructure.cache.token_blacklist_repository import (
    TokenBlacklistRepository,
)
from app.infrastructure.persistence.db_provider import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    ValidateTokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> AuthService:
    token_blacklist_repository = TokenBlacklistRepository(redis)

    return AuthService(db, token_blacklist_repository)


def extract_bearer_token(authorization: str | None) -> str:
    if authorization is None or not authorization.strip():
        raise TokenRequiredError()

    if not authorization.startswith("Bearer "):
        raise InvalidTokenError()

    token = authorization.replace("Bearer ", "", 1).strip()

    if not token:
        raise TokenRequiredError()

    return token


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "sso-service"}


@router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register_user(
        username=data.username,
        password=data.password,
        role=data.role,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login_user(
        username=data.username,
        password=data.password,
    )


@router.post("/validate", response_model=ValidateTokenResponse)
async def validate(
    authorization: str | None = Header(default=None, alias="Authorization"),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = extract_bearer_token(authorization)

    return await auth_service.validate_token(token)


@router.post("/logout")
async def logout(
    authorization: str | None = Header(default=None, alias="Authorization"),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = extract_bearer_token(authorization)

    await auth_service.logout_user(token)

    return {"detail": "Successfully logged out"}
