from uuid import UUID

from litestar import Controller, Response, get

from src.modules.tracks.dto import ITrackBase


class TrackController(Controller):
    path = "/tracks"
    tags = ["Tracks"]

    @get("/{id:uuid}")
    async def get_by_id(self, id: UUID) -> ITrackBase: ...

    @get("")
    async def get_paginated(self) -> Response: ...
