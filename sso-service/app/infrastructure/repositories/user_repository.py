from app.infrastructure.models.user_model import UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> UserModel | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.username == username)
        )

        return result.scalar_one_or_none()

    async def create_user(
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

        return user
