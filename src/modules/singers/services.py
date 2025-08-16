from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.modules.singers.models import SingerModel


class SingerService(SQLAlchemyAsyncRepositoryService[SingerModel]):
    class Repository(SQLAlchemyAsyncRepository[SingerModel]):
        model_type = SingerModel

    repository_type = Repository
