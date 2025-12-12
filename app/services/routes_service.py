from app.models import UpstreamMapping, GetAllRoutesResponse
from app.utils.redis_client import redis_client, Namespace


def upsert_route(req: UpstreamMapping):
    redis_client.set_model(Namespace.UPSTREAMS, req.prefix, req)


def delete_route(req: UpstreamMapping):
    redis_client.delete(Namespace.UPSTREAMS, req.prefix)


def get_all_routes() -> GetAllRoutesResponse:
    upstreams = redis_client.get_all_models(Namespace.UPSTREAMS, UpstreamMapping)
    routes = []

    for upstream in upstreams.values():
        routes.append(upstream)

    return GetAllRoutesResponse(
        routes=routes,
    )
