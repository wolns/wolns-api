import litestar
from dishka.integrations.litestar import (
    DishkaRouter,
    setup_dishka,
)
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from src.core.database import alchemy
from src.core.di import container
from src.core.exceptions import AppError, app_error_handler, generic_handler
from src.core.security import jwt_auth
from src.modules import controllers

dishka_controllers = DishkaRouter("", route_handlers=controllers)

app: litestar.Litestar = Litestar(
    plugins=[alchemy],
    route_handlers=[dishka_controllers],
    # dependencies={"current_player_id": Provide(get_current_player_id)},
    exception_handlers={AppError: app_error_handler, 500: generic_handler},
    on_app_init=[jwt_auth.on_app_init],
    cors_config=CORSConfig(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count"],
    ),
    openapi_config=OpenAPIConfig(
        title="wolns API",
        description="API for wolns",
        version="0.0.1",
        path="/docs",
        render_plugins=[SwaggerRenderPlugin()],
    ),
)

setup_dishka(container=container, app=app)
