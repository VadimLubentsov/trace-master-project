from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.cache.token_blacklist_repository import (
    TokenBlacklistRepository,
)
from app.infrastructure.models.user_model import UserModel
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_service import (
    create_access_token,
    decode_access_token,
)
from app.infrastructure.security.password_service import hash_password, verify_password
from app.schemas.auth import TokenResponse, UserResponse, ValidateTokenResponse


class AuthService:
    def __init__(
        self,
        db: AsyncSession,
        token_blacklist_repository: TokenBlacklistRepository,
    ):
        self.db = db
        self.user_repository = UserRepository(db)
        self.token_blacklist_repository = token_blacklist_repository

    async def register_user(
        self,
        username: str,
        password: str,
        role: str = "user",
    ) -> UserResponse | None:
        existing_user = await self.user_repository.get_by_username(username)

        if existing_user is not None:
            return None

        hashed_password = hash_password(password)

        try:
            user = await self.user_repository.create_user(
                username=username,
                hashed_password=hashed_password,
                role=role,
            )

            await self.db.commit()
            await self.db.refresh(user)

            return self._to_user_response(user)

        except Exception:
            await self.db.rollback()
            raise

    async def login_user(
        self,
        username: str,
        password: str,
    ) -> TokenResponse | None:
        user = await self.user_repository.get_by_username(username)

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "role": user.role,
            }
        )

        return TokenResponse(access_token=access_token)

    async def validate_token(self, token: str) -> ValidateTokenResponse:
        if await self.token_blacklist_repository.is_token_blacklisted(token):
            return ValidateTokenResponse(valid=False)

        payload = decode_access_token(token)

        if payload is None:
            return ValidateTokenResponse(valid=False)

        return ValidateTokenResponse(
            valid=True,
            user_id=payload.get("user_id"),
            username=payload.get("sub"),
            role=payload.get("role"),
        )

    async def logout_user(self, token: str) -> bool:
        payload = decode_access_token(token)

        if payload is None:
            return False

        ttl_seconds = self._get_token_ttl_seconds(payload)

        if ttl_seconds <= 0:
            return False

        await self.token_blacklist_repository.add_token(
            token=token,
            ttl_seconds=ttl_seconds,
        )

        return True

    def _get_token_ttl_seconds(self, payload: dict) -> int:
        token_exp = payload.get("exp")

        if token_exp is None:
            return 0

        now_timestamp = int(datetime.now(UTC).timestamp())

        return int(token_exp) - now_timestamp

    def _to_user_response(self, user: UserModel) -> UserResponse:
        return UserResponse(
            id=user.id,
            username=user.username,
            role=user.role,
            is_active=user.is_active,
        )
