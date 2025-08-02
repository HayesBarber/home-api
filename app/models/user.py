from pydantic import BaseModel
from typing import List

class CreateUserRequest(BaseModel):
    name: str
    public_key: str

class DeleteUserRequest(BaseModel):
    name: str

class GetUsersResponse(BaseModel):
    users: List[str]
