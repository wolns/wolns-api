from typing import TYPE_CHECKING, List

from advanced_alchemy.base import UUIDAuditBase
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
