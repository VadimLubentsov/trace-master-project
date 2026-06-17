from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.use_cases.login_user import login_user
from app.application.use_cases.register_user import register_user
from app.application.use_cases.validate_token import validate_token
from app.infrastructure.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    ValidateTokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "sso-service"}


@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(
        db=db,
        username=data.username,
        password=data.password,
        role=data.role,
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    access_token = login_user(
        db=db,
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
def validate(authorization: str = Header(..., alias="Authorization")):
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
