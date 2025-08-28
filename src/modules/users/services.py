from typing import Any

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, schema_dump

from src.core import crypt
from src.core.exceptions import NotAuthorizedException
from src.modules.users.dto import IUserSignUp
from src.modules.users.models import UserModel


class UserService(SQLAlchemyAsyncRepositoryService[UserModel]):
    class Repository(SQLAlchemyAsyncRepository[UserModel]):
        model_type = UserModel

    repository_type = Repository

    async def create(self, data: IUserSignUp) -> UserModel:  # type: ignore[override]
        dumped = schema_dump(data)
        dumped = await self._populate_with_hashed_password(dumped)
        return await super().create(dumped)

    async def _populate_with_hashed_password(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        if isinstance(data, dict) and "password" in data:
            password = data.pop("password")
            data.update(hashed_password=await crypt.get_password_hash(password))
        return data

    async def authenticate(self, email: str, password: str) -> UserModel:
        db_obj = await self.get_one_or_none(email=email)
        if not db_obj or not await crypt.verify_password(
            password, db_obj.hashed_password
        ):
            raise NotAuthorizedException()
        return db_obj
