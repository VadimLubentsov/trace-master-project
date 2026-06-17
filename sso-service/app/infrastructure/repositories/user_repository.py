from sqlalchemy.orm import Session

from app.infrastructure.models.user_model import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def create_user(
        self,
        username: str,
        hashed_password: str,
        role: str = "user",
    ) -> UserModel:
        user = UserModel(
            username=username,
            hashed_password=hashed_password,
            role=role,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
