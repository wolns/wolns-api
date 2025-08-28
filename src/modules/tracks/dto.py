from datetime import datetime
from uuid import UUID

from src.core.dto import BaseStruct
from src.core.enums import PlatformEnum


class ITrackBase(BaseStruct):
    id: UUID
    name: str
    singer: str
    url: str
    duration: int


class ITrackUser(ITrackBase):
    is_listening: bool
    platform: PlatformEnum
    listened_at: datetime


class ITracksBase(BaseStruct):
    tracks: list[ITrackBase]


class ITracksUser(BaseStruct):
    tracks: list[ITrackUser]
