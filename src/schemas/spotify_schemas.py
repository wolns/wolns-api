from pydantic import BaseModel
from typing import Optional
from src.schemas.track_schemas import TrackBaseInfo


class SpotifyAuthResponseSchema(BaseModel):
    auth_url: str


class SpotifyRefreshTokenSchema(BaseModel):
    refresh_token: str


class SpotifyCallbackResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class CurrentTrackResponseSchema(BaseModel):
    track: Optional[TrackBaseInfo] = None
    is_playing: bool = False
