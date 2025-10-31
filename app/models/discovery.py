from pydantic import BaseModel


class DiscoverEspRequest(BaseModel):
    passcode: str
    port: int
