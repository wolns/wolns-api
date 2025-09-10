from uuid import UUID

from src.core.dto import BaseStruct
from src.core.enums import FollowStatusEnum
from src.modules.singers.dto import ISingerStats


class IUserSignIn(BaseStruct):
    email: str
    password: str


class IUserSignUp(BaseStruct):
    email: str
    name: str
    password: str


class IUserBase(BaseStruct):
    id: UUID
    name: str
    avatar_url: str | None = None
    status: str | None = None
    yandex_url: str | None = None
    spotify_url: str | None = None


class IUserRead(BaseStruct):
    follow_status: FollowStatusEnum


class IUsersBase(BaseStruct):
    users: list[IUserBase]


class ISingersUser(BaseStruct):
    singers: list[ISingerStats]
