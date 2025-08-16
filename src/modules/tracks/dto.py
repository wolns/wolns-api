from uuid import UUID

from msgspec import Struct

from core.enums import PositionEnum


class ISingerBase(Struct):
    id: UUID
    name: str
    url: str
    image_url: str


class ISingerStats(ISingerBase):
    place: int
    position: PositionEnum
    hours: int
