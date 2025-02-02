from app.core.config import settings

from redis.asyncio import Redis


async def get_redis_client() -> Redis:
    return Redis(host=settings.redis.host, port=settings.redis.port, decode_responses=True)