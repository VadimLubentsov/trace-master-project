from fastapi import APIRouter, Header, HTTPException

from app.application.use_cases.login_user import login_user
from app.application.use_cases.validate_token import validate_token
from app.schemas.auth import LoginRequest, TokenResponse, ValidateTokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "sso-service"}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    access_token = login_user(
        username=data.username,
        password=data.password,
    )

    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return TokenResponse(access_token=access_token)


@router.post("/validate", response_model=ValidateTokenResponse)
def validate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    token = authorization.replace("Bearer ", "")

    result = validate_token(token)

    if not result["valid"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return ValidateTokenResponse(**result)
