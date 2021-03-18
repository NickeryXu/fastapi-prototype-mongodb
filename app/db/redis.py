from fastapi_plugins import RedisSettings

from app.core.config import redis_host, redis_port, redis_password


class RedisAppSettings(RedisSettings):
    redis_host: str = redis_host
    redis_port: int = redis_port
    redis_password: str = redis_password


redis_config = RedisAppSettings()
