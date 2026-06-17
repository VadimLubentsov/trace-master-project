from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool


class ValidateTokenResponse(BaseModel):
    valid: bool
    user_id: int | None = None
    username: str | None = None
    role: str | None = None
