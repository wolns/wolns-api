from collections.abc import Iterable

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.integrations.litestar import LitestarProvider
from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import sqlalchemy_config
from src.core.settings import Settings, get_settings
from src.modules.users.services import UserService


class SettingsProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)


class RequestProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_session(self, request: Request) -> AsyncSession:
        return sqlalchemy_config.provide_session(
            state=request.app.state, scope=request.scope
        )


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_service(self, session: AsyncSession) -> UserService:
        return UserService(session=session)


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        RequestProvider(),
        ServicesProvider(),
        LitestarProvider(),
    )


def create_async_container(*providers: Provider) -> AsyncContainer:
    settings = get_settings()
    return make_async_container(
        *providers,
        context={Settings: settings},
    )


container = create_async_container(*get_providers())
