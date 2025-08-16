from uuid import UUID

from msgspec import Struct


class IUserBase(Struct):
    id: UUID
    name: str
    avatar_url: str
    status: str
    yandex_url: str | None
    spotify_url: str | None
