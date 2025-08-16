from litestar.plugins.sqlalchemy import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)

from src.core.settings import get_settings

DATABASE_URL = get_settings().postgres.url

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=DATABASE_URL,
    before_send_handler="autocommit",
    session_config=AsyncSessionConfig(expire_on_commit=False),
    alembic_config=AlembicAsyncConfig(script_location="./migrations"),
    create_all=False,
)
alchemy = SQLAlchemyPlugin(config=sqlalchemy_config)
