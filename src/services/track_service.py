from uuid import UUID

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.database import get_async_session
from src.models.track_model import Track
from src.repositories.track_repository import TrackRepository


class TrackService:
    def __init__(self, session: AsyncSession):
        self.track_repository = TrackRepository(session)

    async def get_track_by_user_uuid(self, user_uuid: UUID) -> Track | None:
        return await self.track_repository.get_by_user_uuid(user_uuid)

    async def get_recently_updated_track_by_user_uuid(self, user_uuid: UUID) -> Track | None:
        return await self.track_repository.get_recently_updated_by_user_uuid(user_uuid)


async def get_track_service(session: AsyncSession = Depends(get_async_session)) -> TrackService:
    return TrackService(session)
