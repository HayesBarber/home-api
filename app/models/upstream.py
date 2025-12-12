from pydantic import BaseModel


class UpstreamMapping(BaseModel):
    prefix: str
    base_url: str


class GetAllRoutesResponse(BaseModel):
    routes: list[UpstreamMapping]
