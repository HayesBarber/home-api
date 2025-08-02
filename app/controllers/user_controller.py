from fastapi import APIRouter
from app.models import CreateUserRequest, DeleteUserRequest
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(req: CreateUserRequest):
    return user_service.create_user(req)

@router.delete("/")
def delete_user(req: DeleteUserRequest):
    return user_service.delete_user(req)

@router.get("/")
def get_users():
    return user_service.get_all_users()
