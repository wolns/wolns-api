from uuid import UUID

from src.core.dto import BaseStruct
from src.core.enums import PositionEnum


class ISingerBase(BaseStruct):
    id: UUID
    name: str
    url: str
    image_url: str


class ISingerStats(ISingerBase):
    place: int
    position: PositionEnum
    hours: int
