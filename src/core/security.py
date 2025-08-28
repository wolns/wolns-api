from uuid import UUID

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token

from src.core.database import sqlalchemy_config
from src.core.settings import get_settings
from src.modules.users.models import UserModel
from src.modules.users.services import UserService


async def retrieve_user_handler(
    token: Token,
    connection: ASGIConnection,
) -> UserModel | None:
    db_session = sqlalchemy_config.provide_session(
        state=connection.app.state, scope=connection.scope
    )
    user_service = UserService(session=db_session)
    user_id = UUID(token.sub)
    try:
        user = await user_service.get(item_id=user_id)
        return user
    except (TypeError, ValueError):
        return None


EXCLUDED_PATH = [
    "/docs",
    "/auth",
]

jwt_auth = JWTAuth[UserModel](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=get_settings().jwt.secret_key,
    exclude=EXCLUDED_PATH,
)
