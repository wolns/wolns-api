from fastapi import APIRouter, Depends, Query

from src.schemas.account_schemas import VKAccountBodySchema
from src.schemas.vk_schemas import VKAuthResponseSchema
from src.services.music_services.vk_service import VKService, get_vk_service

vk_router = APIRouter(prefix="/vk", tags=["VK"])


@vk_router.get("/login")
async def vk_login(vk_service: VKService = Depends(get_vk_service)) -> VKAuthResponseSchema:
    auth_url = vk_service.get_auth_url()
    return VKAuthResponseSchema(auth_url=auth_url)


@vk_router.get("/callback")
async def vk_callback(
    code: str = Query(...),
    device_id: str = Query(...),
    state: str = Query(...),
    vk_service: VKService = Depends(get_vk_service),
) -> VKAccountBodySchema:
    return await vk_service.get_tokens(code, device_id, state)
