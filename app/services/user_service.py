from app.utils.redis_client import redis_client, Namespace
from app.models import CreateUserRequest, DeleteUserRequest, GetUsersResponse

def create_user(req: CreateUserRequest) -> GetUsersResponse:
    redis_client.set(Namespace.USERS, req.name, req.public_key)
    return get_all_users()

def delete_user(req: DeleteUserRequest) -> GetUsersResponse:
    redis_client.delete(Namespace.USERS, req.name)
    return get_all_users()

def get_all_users() -> GetUsersResponse:
    users = redis_client.get_all(Namespace.USERS)
    as_list =  list(users.keys())

    return GetUsersResponse(
        users=as_list
    )
