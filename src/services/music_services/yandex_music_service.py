from typing import Optional

import aiohttp
import json
import random
import string
from yandex_music import ClientAsync

from src.core.config import get_yandex_music_settings
from src.core.exceptions import TokenExpiredException
from src.schemas.account_schemas import YandexMusicAccountBodySchema
from src.schemas.track_schemas import ServiceType, TrackBaseInfo
from src.schemas.yandex_schemas import YandexMusicTestSchema
from src.services.music_service import MusicService
from src.services.music_services.base_oauth2_service import BaseOAuth2Service
from src.services.music_services.yandex_ynison_protocol import YnisonProtocol


class YandexMusicService(MusicService, BaseOAuth2Service):
    """Service for interacting with Yandex Music API"""
    
    service_type = ServiceType.YANDEX_MUSIC

    @property
    def scope(self) -> str:
        """Override base method since Yandex doesn't use scope"""
        return ""

    def __init__(self):
        settings = get_yandex_music_settings()
        self.ynison = YnisonProtocol()
        super().__init__(
            client_id=settings.yandex_music_client_id,
            client_secret=settings.yandex_music_client_secret,
            redirect_uri=settings.yandex_music_redirect_uri,
            auth_url="https://oauth.yandex.ru/authorize",
            token_url="https://oauth.yandex.ru/token",
        )

    def get_auth_url(self) -> str:
        """Override base method since Yandex doesn't use scope"""
        return (
            f"{self.auth_url}"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
        )

    async def get_tokens(self, code: str) -> YandexMusicAccountBodySchema:
        """Exchange authorization code for access and refresh tokens"""
        data = {"grant_type": "authorization_code", "code": code}
        response_data = await self._make_token_request(data, "Failed to get tokens")
        return YandexMusicAccountBodySchema.model_validate(response_data)

    async def refresh_tokens(self, refresh_token: str) -> YandexMusicAccountBodySchema:
        """Refresh access token using refresh token"""
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response_data = await self._make_token_request(data, "Failed to refresh tokens")
        return YandexMusicAccountBodySchema.model_validate(response_data)

    async def _get_preynison(self, access_token: str):
        """Get pre-ynison data for websocket connection"""
        device_id = self.ynison.generate_device_id()
        ws_proto, proto_str = self.ynison.create_websocket_protocol(device_id)
        
        session = aiohttp.ClientSession()
        ws = await session.ws_connect(
            url=self.ynison.YNISON_REDIRECT_URL,
            headers={
                "Sec-WebSocket-Protocol": f"Bearer, v2, {proto_str}",
                "Origin": self.ynison.ORIGIN,
                "Authorization": f"OAuth {access_token}",
            },
        )
        
        try:
            recv = await ws.receive()
            data = json.loads(recv.data)

            if not data["redirect_ticket"]:
                raise TokenExpiredException

            new_ws_proto = {**ws_proto, "Ynison-Redirect-Ticket": data["redirect_ticket"]}
            return session, self.ynison.get_initial_state(device_id), data["host"], json.dumps(new_ws_proto)
        finally:
            await ws.close()

    async def get_current_track(self, obj: YandexMusicAccountBodySchema | YandexMusicTestSchema) -> Optional[TrackBaseInfo]:
        """Get user's currently playing track"""
        session, to_send, host, proto = await self._get_preynison(obj.access_token)
        
        try:
            async with session.ws_connect(
                url=f"wss://{host}/ynison_state.YnisonStateService/PutYnisonState",
                headers={
                    "Sec-WebSocket-Protocol": f"Bearer, v2, {proto}",
                    "Origin": self.ynison.ORIGIN,
                    "Authorization": f"OAuth {obj.access_token}",
                },
                method="GET",
            ) as ws:
                await ws.send_str(json.dumps(to_send))
                recv = await ws.receive()
                ynison = json.loads(recv.data)

                client = ClientAsync(token=obj.access_token)
                await client.init()
                
                return await self._parse_track_data(client, ynison)
        finally:
            await session.close()

    async def _parse_track_data(self, client: ClientAsync, ynison: dict) -> Optional[TrackBaseInfo]:
        """Parse track data from Ynison response"""
        track_data = await self._get_track_from_ynison(client, ynison)
        
        if not track_data or not track_data["track"] or track_data["paused"]:
            return None

        return TrackBaseInfo(
            title=track_data["track"].title,
            artists=", ".join(x.name for x in track_data["track"].artists),
            cover="https://" + track_data["track"].cover_uri.replace("%%", "400x400"),
            duration_ms=track_data["duration_ms"],
            progress_ms=track_data["progress_ms"],
        )

    async def _get_track_from_ynison(self, client: ClientAsync, ynison: dict) -> Optional[dict]:
        """Extract track information from Ynison data"""
        try:
            queue = ynison["player_state"]["player_queue"]
            track = queue["playable_list"][queue["current_playable_index"]]
            
            track_info = (await client.tracks(track["playable_id"]))[0]
            
            return {
                "paused": ynison["player_state"]["status"]["paused"],
                "duration_ms": ynison["player_state"]["status"]["duration_ms"],
                "progress_ms": ynison["player_state"]["status"]["progress_ms"],
                "entity_id": queue["entity_id"],
                "entity_type": queue["entity_type"],
                "track": track_info,
            }
        except (IndexError, Exception) as e:
            return None


async def get_yandex_music_service() -> YandexMusicService:
    return YandexMusicService()
