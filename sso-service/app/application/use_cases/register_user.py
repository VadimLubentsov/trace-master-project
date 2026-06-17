from sqlalchemy.orm import Session

from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.password_service import hash_password


def register_user(
    db: Session,
    username: str,
    password: str,
    role: str = "user",
):
    user_repository = UserRepository(db)

    existing_user = user_repository.get_by_username(username)

    if existing_user is not None:
        return None

    hashed_password = hash_password(password)

    user = user_repository.create_user(
        username=username,
        hashed_password=hashed_password,
        role=role,
    )

    return user
