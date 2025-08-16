from typing import TYPE_CHECKING, List
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ..singers.models import SingerModel
    from ..users.models import UserModel


class TrackModel(UUIDAuditBase):
    __tablename__ = "tracks"

    name: Mapped[str] = mapped_column(nullable=False)
    spotify_url: Mapped[str] = mapped_column(nullable=True)
    yandex_url: Mapped[str] = mapped_column(nullable=True)
    spotify_image_url: Mapped[str] = mapped_column(nullable=True)
    yandex_image_url: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(nullable=False)
    singers: Mapped[List["TrackSingerModel"]] = relationship(
        "TrackSingerModel",
        back_populates="track",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    listenings: Mapped[List["ListeningModel"]] = relationship(
        "ListeningModel",
        back_populates="track",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class TrackSingerModel(UUIDAuditBase):
    __tablename__ = "track_singers"
    __table_args__ = (
        UniqueConstraint("track_id", "singer_id", name="uq_track_singer"),
    )

    track_id: Mapped[UUID] = mapped_column(
        ForeignKey("tracks.id", ondelete="CASCADE"), index=True, nullable=False
    )
    singer_id: Mapped[UUID] = mapped_column(
        ForeignKey("singers.id", ondelete="CASCADE"), index=True, nullable=False
    )

    track: Mapped["TrackModel"] = relationship("TrackModel", back_populates="singers")
    singer: Mapped["SingerModel"] = relationship("SingerModel", lazy="selectin")


class ListeningModel(UUIDAuditBase):
    __tablename__ = "listenings"

    track_id: Mapped[UUID] = mapped_column(
        ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    track: Mapped["TrackModel"] = relationship(
        "TrackModel", back_populates="listenings"
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", lazy="selectin", back_populates="listenings"
    )
