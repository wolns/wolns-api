import base64
import hashlib
import secrets
from urllib.parse import urlencode

import aiohttp
from fastapi import HTTPException

from src.core.config import get_vk_settings
from src.schemas.account_schemas import VKAccountBodySchema
from src.schemas.track_schemas import ServiceType, TrackBaseInfo
from src.services.music_service import MusicService

pkce_store = {}


class VKService(MusicService):
    service_type = ServiceType.VK

    def __init__(self):
        vk_settings = get_vk_settings()
        self.client_id = vk_settings.vk_client_id
        self.redirect_uri = vk_settings.vk_redirect_uri
        self.auth_url = "https://id.vk.com/authorize"
        self.token_url = "https://id.vk.com/oauth2/auth"
        self.api_base_url = "https://api.vk.com/method"

    def get_auth_url(self) -> tuple[str, str]:
        state = secrets.token_urlsafe(32)
        code_verifier = secrets.token_urlsafe(32)
        digest = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(digest).decode().rstrip("=")
        pkce_store[state] = code_verifier

        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "email phone",
            "response_type": "code",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{self.auth_url}?{urlencode(auth_params)}"

    async def get_tokens(self, code: str, device_id: str, state: str) -> VKAccountBodySchema:
        code_verifier = pkce_store.pop(state, None)
        if not code_verifier:
            raise HTTPException(status_code=400, detail="Invalid or missing PKCE state")

        data = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
            "device_id": device_id,
            "redirect_uri": self.redirect_uri,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to get tokens")
                return VKAccountBodySchema.model_validate(await response.json())

    async def get_current_track(self, obj: VKAccountBodySchema) -> TrackBaseInfo | None:
        pass


async def get_vk_service() -> VKService:
    return VKService()
