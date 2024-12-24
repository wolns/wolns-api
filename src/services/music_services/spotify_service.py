from typing import Optional, Dict, Any

import aiohttp
from fastapi import HTTPException

from src.core.config import get_spotify_settings
from src.core.exceptions import TokenExpiredException
from src.schemas.account_schemas import SpotifyAccountBodySchema
from src.schemas.track_schemas import ServiceType, TrackBaseInfo
from src.services.music_service import MusicService
from src.services.music_services.base_oauth2_service import BaseOAuth2Service


class SpotifyService(MusicService, BaseOAuth2Service):
    """Service for interacting with Spotify API"""
    
    service_type = ServiceType.SPOTIFY
    API_BASE_URL = "https://api.spotify.com/v1"

    @property
    def scope(self) -> str:
        return "user-read-currently-playing"

    def __init__(self):
        settings = get_spotify_settings()
        BaseOAuth2Service.__init__(
            self,
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
            redirect_uri=settings.spotify_redirect_uri,
            auth_url="https://accounts.spotify.com/authorize",
            token_url="https://accounts.spotify.com/api/token",
        )

    async def get_tokens(self, code: str) -> SpotifyAccountBodySchema:
        """Exchange authorization code for access and refresh tokens"""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response_data = await self._make_token_request(data, "Failed to get tokens")
        return SpotifyAccountBodySchema.model_validate(response_data)

    async def refresh_tokens(self, refresh_token: str) -> SpotifyAccountBodySchema:
        """Refresh access token using refresh token"""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response_data = await self._make_token_request(data, "Failed to refresh token")
        
        # Spotify doesn't always return a new refresh token
        if "refresh_token" not in response_data:
            response_data["refresh_token"] = refresh_token

        return SpotifyAccountBodySchema.model_validate(response_data)

    async def _make_api_request(self, endpoint: str, access_token: str) -> Dict[str, Any]:
        """Make an authenticated request to the Spotify API"""
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.API_BASE_URL}/{endpoint.lstrip('/')}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 401:
                    raise TokenExpiredException
                
                if response.status not in (200, 204, 404):
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Spotify API request failed: {response.status}"
                    )
                
                return await response.json() if response.status == 200 else {}

    async def get_current_track(self, obj: SpotifyAccountBodySchema) -> Optional[TrackBaseInfo]:
        """Get user's currently playing track"""
        try:
            data = await self._make_api_request("me/player/currently-playing", obj.access_token)
            return self._parse_track_data(data) if data else None
        except HTTPException as e:
            if e.status_code in (204, 404):
                return None
            raise

    def _parse_track_data(self, data: dict) -> Optional[TrackBaseInfo]:
        """Parse track data from Spotify API response"""
        if not data.get("item") or not data.get("is_playing"):
            return None

        track = data["item"]
        return TrackBaseInfo(
            title=track["name"],
            artists=", ".join(artist["name"] for artist in track["artists"]),
            cover=track["album"]["images"][0]["url"],
            duration_ms=track["duration_ms"],
            progress_ms=data.get("progress_ms"),
        )


async def get_spotify_service() -> SpotifyService:
    return SpotifyService()
