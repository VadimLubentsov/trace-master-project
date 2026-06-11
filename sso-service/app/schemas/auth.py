from pydantic import BaseModel


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
    role: str | None = None
