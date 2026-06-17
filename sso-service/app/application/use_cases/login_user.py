from sqlalchemy.orm import Session

from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_service import create_access_token
from app.infrastructure.security.password_service import verify_password


def login_user(db: Session, username: str, password: str) -> str | None:
    user_repository = UserRepository(db)

    user = user_repository.get_by_username(username)

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

    return access_token
