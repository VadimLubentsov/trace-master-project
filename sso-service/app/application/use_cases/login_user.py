from app.domain.entities.user import User
from app.infrastructure.security.jwt_service import create_access_token

fake_user = User(
    id=1,
    username="vadim",
    password="12345",
    role="user",
)


def login_user(username: str, password: str) -> str | None:
    if username != fake_user.username:
        return None

    if password != fake_user.password:
        return None

    access_token = create_access_token(
        data={
            "sub": fake_user.username,
            "user_id": fake_user.id,
            "role": fake_user.role,
        }
    )

    return access_token
