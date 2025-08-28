from typing import TYPE_CHECKING, List
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ..tracks.models import ListeningModel


class UserModel(UUIDAuditBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(nullable=True)
    status: Mapped[str | None] = mapped_column(nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(nullable=True)

    listenings: Mapped[List["ListeningModel"]] = relationship(
        "ListeningModel", back_populates="user", foreign_keys="ListeningModel.user_id"
    )

    following: Mapped[List["FollowModel"]] = relationship(
        "FollowModel",
        back_populates="from_user",
        foreign_keys="FollowModel.from_user_id",
    )
    followers: Mapped[List["FollowModel"]] = relationship(
        "FollowModel",
        back_populates="to_user",
        foreign_keys="FollowModel.to_user_id",
    )


class FollowModel(UUIDAuditBase):
    __tablename__ = "follows"
    __table_args__ = (UniqueConstraint("from_user_id", "to_user_id", name="uq_follow"),)

    from_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    to_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    from_user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="following", foreign_keys=[from_user_id]
    )
    to_user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="followers", foreign_keys=[to_user_id]
    )
