from pydantic import BaseModel


class VKAuthResponseSchema(BaseModel):
    auth_url: str
