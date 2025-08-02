from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    public_key: str

class DeleteUserRequest(BaseModel):
    name: str
