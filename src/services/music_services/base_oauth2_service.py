import base64
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import aiohttp
from fastapi import HTTPException

from src.schemas.account_schemas import AccountBodySchema


class BaseOAuth2Service(ABC):
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, auth_url: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url

    @property
    @abstractmethod
    def scope(self) -> str:
        """OAuth2 scope required by the service"""
        pass

    def get_auth_url(self) -> str:
        """Generate authorization URL for OAuth2 flow"""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        return f"{self.auth_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def _get_auth_header(self) -> str:
        """Generate basic auth header from client credentials"""
        auth_string = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(auth_string.encode()).decode()

    def _get_token_headers(self) -> Dict[str, str]:
        """Get headers for token requests"""
        return {
            "Authorization": f"Basic {self._get_auth_header()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    async def _make_token_request(self, data: Dict[str, str], error_message: str) -> Dict[str, Any]:
        """Make a token request to the OAuth2 server"""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.token_url, headers=self._get_token_headers(), data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail=error_message)
                return await response.json()

    @abstractmethod
    async def get_tokens(self, code: str) -> AccountBodySchema:
        """Exchange authorization code for access and refresh tokens"""
        pass

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str) -> AccountBodySchema:
        """Refresh access token using refresh token"""
        pass 