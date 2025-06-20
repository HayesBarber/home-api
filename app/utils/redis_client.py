from enum import Enum
import os
import redis
from typing import Optional, Any, Type, TypeVar, Dict, Tuple, Iterator, List
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

class Namespace(str, Enum):
    DEVICE_CONFIG = "device_config"
    USERS = "users"
    CHALLENGES = "challenges"
    API_KEYS = "api_keys"
    ROUTINES = "routines"
    THEMES = "themes"

class TTL(int, Enum):
    DEVICE_CONFIG = 15 * 60
    API_KEYS = 5 * 60

class RedisClient:
    def __init__(self, redis_url: Optional[str] = None):
        if redis_url is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self._redis = redis.from_url(redis_url)

    def _make_key(self, namespace: Namespace, key: str) -> str:
        return f"{namespace.value}:{key}"
    
    def get_ttl_for_namespace(self, ns: Namespace) -> Optional[int]:
        try:
            return TTL[ns.name].value
        except KeyError:
            return None

    def get(self, namespace: Namespace, key: str) -> Optional[str]:
        full_key = self._make_key(namespace, key)
        value = self._redis.get(full_key)
        return value.decode() if value else None

    def set(self, namespace: Namespace, key: str, value: Any):
        full_key = self._make_key(namespace, key)
        val = value if isinstance(value, (str, bytes)) else str(value)
        self._redis.set(full_key, val, ex=self.get_ttl_for_namespace(namespace))

    def delete(self, namespace: Namespace, key: str):
        full_key = self._make_key(namespace, key)
        self._redis.delete(full_key)

    def get_model(self, namespace: Namespace, key: str, model: Type[T]) -> Optional[T]:
        raw = self.get(namespace, key)
        if not raw:
            return None
        try:
            return model.model_validate_json(raw)
        except ValidationError:
            print(f"Error parsing model json for key {self._make_key(namespace, key)}")
            return None

    def set_model(self, namespace: Namespace, key: str, model_instance: BaseModel):
        self.set(namespace, key, model_instance.model_dump_json())

    def _get_all_raw(self, namespace: Namespace) -> Iterator[Tuple[str, bytes]]:
        pattern = f"{namespace.value}:*"
        full_keys_bytes = self._redis.keys(pattern)

        if not full_keys_bytes:
            return

        full_keys = [k.decode() for k in full_keys_bytes]
        values_bytes = self._redis.mget(full_keys)

        for full_key, value_bytes in zip(full_keys, values_bytes):
            if value_bytes is not None:
                # The '1' in split ensures we only split on the first colon
                original_key = full_key.split(':', 1)[1]
                yield original_key, value_bytes

    def get_all(self, namespace: Namespace) -> Dict[str, str]:
        return {
            key: value.decode()
            for key, value in self._get_all_raw(namespace)
        }

    def get_all_models(self, namespace: Namespace, model: Type[T]) -> Dict[str, T]:
        all_models = {}
        for original_key, value_bytes in self._get_all_raw(namespace):
            try:
                all_models[original_key] = model.model_validate_json(value_bytes)
            except ValidationError:
                full_key_for_error = f"{namespace.value}:{original_key}"
                print(f"Error parsing model json for key {full_key_for_error}. Skipping this entry.")
            except Exception as e:
                full_key_for_error = f"{namespace.value}:{original_key}"
                print(f"An unexpected error occurred for key {full_key_for_error}: {e}")
        return all_models
    
    def set_all_models(self, namespace: Namespace, models: List[T], key_field: str) -> int:
        if not models:
            return 0

        try:
            pipeline_data = {
                f"{namespace.value}:{str(getattr(model, key_field))}": model.model_dump_json()
                for model in models
            }
        except AttributeError as e:
            raise AttributeError(f"The key_field '{key_field}' does not exist on a provided model.") from e

        if not pipeline_data:
            return 0

        ttl = self.get_ttl_for_namespace(namespace)

        pipe = self._redis.pipeline()
        for key, value in pipeline_data.items():
            pipe.set(key, value)
            if ttl is not None:
                pipe.expire(key, ttl)
        pipe.execute()

        return len(pipeline_data)

redis_client = RedisClient()
