from typing import TYPE_CHECKING, List
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ..tracks.models import ListeningModel


class UserModel(UUIDAuditBase):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    listenings: Mapped[List["ListeningModel"]] = relationship(
        "ListeningModel", back_populates="user"
    )

    following: Mapped[List["FollowModel"]] = relationship(
        "FollowModel", back_populates="from_user"
    )
    followers: Mapped[List["FollowModel"]] = relationship(
        "FollowModel", back_populates="to_user"
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

    from_user: Mapped["UserModel"] = relationship("UserModel", back_populates="singers")
    to_user: Mapped["UserModel"] = relationship("UserModel", back_populates="singers")
