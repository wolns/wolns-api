from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(UUIDAuditBase):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
