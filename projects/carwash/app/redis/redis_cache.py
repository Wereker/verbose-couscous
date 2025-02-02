from redis.asyncio import Redis
from typing import Optional
import json


class RedisCache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client


    async def get_order_metadata(self, order_id: int) -> Optional[int]:
        """Получить мета-данные из заказа из Redis"""
        data = await self.redis.get(f"order:{order_id}:metadata")

        if data:
            return json.loads(data) if data else None
        return None
    

    async def set_order_metadata(self, order_id: int, metadata: dict):
        """Установить мета-данные заказа в Redis"""
        await self.redis.set(f"order:{order_id}:metadata", json.dumps(metadata), ex=3600)

    
    async def delete_order_metadata(self, order_id: int):
        """Удалить мета-данные заказа из Redis"""
        await self.redis.delete(f"order:{order_id}:metadata")