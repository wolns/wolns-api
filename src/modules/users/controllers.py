from typing import Any
from uuid import UUID

from dishka import FromDishka
from litestar import Controller, Request, Response, delete, get, post
from litestar.security.jwt import Token

from src.core.security import jwt_auth
from src.modules.tracks.dto import ITracksUser
from src.modules.users.dto import (
    ISingersUser,
    IUserBase,
    IUserRead,
    IUserSignIn,
    IUserSignUp,
)
from src.modules.users.models import UserModel
from src.modules.users.services import UserService


class UserController(Controller):
    path = "/users"
    tags = ["Users"]

    @post("/sign-up", exclude_from_auth=True)
    async def signup(
        self, user_service: FromDishka[UserService], data: IUserSignUp
    ) -> Response[IUserBase]:
        user = await user_service.create(data)
        user_dto = user_service.to_schema(user, schema_type=IUserBase)
        return jwt_auth.login(
            identifier=str(user.id),
            response_body=user_dto,
        )

    @post("/sign-in", exclude_from_auth=True)
    async def signin(
        self, user_servide: FromDishka[UserService], data: IUserSignIn
    ) -> Response[IUserBase]:
        user = await user_servide.authenticate(email=data.email, password=data.password)
        user_dto = user_servide.to_schema(user, schema_type=IUserBase)
        return jwt_auth.login(
            identifier=str(user.id),
            response_body=user_dto,
        )

    @post("/me")
    async def get_me(
        self,
        request: Request[UserModel, Token, Any],
        user_service: FromDishka[UserService],
    ) -> IUserBase:
        user_dto = user_service.to_schema(request.user, schema_type=IUserBase)
        return user_dto

    @get("/{id:uuid}")
    async def get_by_id(
        self,
        id: UUID,
        request: Request[UserModel, Token, Any],
    ) -> IUserRead: ...

    @post("/{id:uuid}/follow")
    async def follow(
        self,
        id: UUID,
        request: Request[UserModel, Token, Any],
    ) -> None: ...

    @delete("/{id:uuid}/follow")
    async def unfollow(
        self,
        id: UUID,
        request: Request[UserModel, Token, Any],
    ) -> None: ...

    @get("/{id:uuid}/singers/stats")
    async def get_singers_stats(
        self,
        id: UUID,
        request: Request[UserModel, Token, Any],
        page: int = 1,
        page_size: int = 20,
    ) -> ISingersUser: ...

    @get("/{id:uuid}/tracks")
    async def get_tracks(
        self,
        id: UUID,
        request: Request[UserModel, Token, Any],
        page: int = 1,
        page_size: int = 20,
    ) -> ITracksUser: ...
