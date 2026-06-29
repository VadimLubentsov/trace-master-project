from pydantic import BaseModel, Field

from app.application.enums.user_role import UserRole


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    role: UserRole = UserRole.USER


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ValidateTokenResponse(BaseModel):
    valid: bool
    user_id: int | None = None
    username: str | None = None
    role: UserRole | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    is_active: bool
