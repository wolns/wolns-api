from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship

from src.schemas.track_schemas import ServiceType
from .account_model import BaseAccount

if TYPE_CHECKING:
    from .user_model import User


class YandexMusicAccount(BaseAccount, table=True):
    service_type: ClassVar[ServiceType] = ServiceType.YANDEX_MUSIC

    access_token: str = Field(sa_column=Column(String(400), nullable=False))
    refresh_token: str = Field(sa_column=Column(String(400), nullable=False))

    user: "User" = Relationship(
        back_populates="yandex_music_account",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
