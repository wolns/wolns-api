from uuid import UUID

from core.enums import PositionEnum
from src.core.dto import BaseStruct


class ISingerBase(BaseStruct):
    id: UUID
    name: str
    url: str
    image_url: str


class ISingerStats(ISingerBase):
    place: int
    position: PositionEnum
    hours: int
