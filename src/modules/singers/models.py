from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column


class SingerModel(UUIDAuditBase):
    __tablename__ = "singers"

    name: Mapped[str] = mapped_column(nullable=False)
    spotify_url: Mapped[str] = mapped_column(nullable=True)
    yandex_url: Mapped[str] = mapped_column(nullable=True)
    spotify_image_url: Mapped[str] = mapped_column(nullable=True)
    yandex_image_url: Mapped[str] = mapped_column(nullable=True)
