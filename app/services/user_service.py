from app.utils.redis_client import redis_client, Namespace
from app.models import CreateUserRequest, DeleteUserRequest

def create_user(req: CreateUserRequest):
    redis_client.set(Namespace.USERS, req.name, req.public_key)

def delete_user(req: DeleteUserRequest):
    redis_client.delete(Namespace.USERS, req.name)

def get_all_users():
    pass
